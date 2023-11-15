let userRole;
let chatbots;
let favoriteChatbots = new Set();
let tagFilter = new Set();
const itemsPerPage = 15;
let currentPage = 1;
let searchFilter = '';
let favoritesOnly = false;
let filteredChatbots = [];
let favoriteColor = 'rgba(255, 105, 97, 1)';
let notFavoriteColor = 'rgba(0, 0, 0, 5)';


window.onload = async function () {
  console.log('Window onload function called');

  const roleResponse = await fetch('/api/current_user_role');
  const roleData = await roleResponse.json();
  userRole = roleData.role;
  console.log('User role:', userRole);

  const response = await fetch('/api/chatbots');
  chatbots = await response.json();
  console.log('Chatbots:', chatbots);

  const favoritesResponse = await fetch('/api/favorites');
  const favorites = await favoritesResponse.json();
  favoriteChatbots = new Set(favorites);
  console.log('Favorites:', favorites);

  const tagsResponse = await fetch('/api/common_tags');
  const commonTags = await tagsResponse.json();

  renderTagButtons(commonTags);
  renderChatbots();
  renderPagination();
};

function renderTagButtons(tags) {
  const container = document.querySelector('.container-tagbuttons');
  tags.forEach(tag => {
      const button = document.createElement('button');
      button.textContent = tag;
      button.classList.add('button-glass');
      button.onclick = () => applyTagFilter(tag);
      container.appendChild(button);
  });
}


function renderChatbots() {
    console.log("renderChatbots function called");

    const votedChatbots = JSON.parse(localStorage.getItem("votedChatbots")) || [];

    filteredChatbots = chatbots.filter(chatbot => {
        const nameMatchesSearch = chatbot.name.toLowerCase().includes(searchFilter.toLowerCase());
        const tagMatchesSearch = chatbot.tags.some(tag => tag.toLowerCase().includes(searchFilter.toLowerCase()));
        const matchesSearch = nameMatchesSearch || tagMatchesSearch; 

        const isFavorite = favoriteChatbots.has(chatbot.id);
        const tagMatchesFilter = Array.from(tagFilter).every(val => chatbot.tags.includes(val));
        const hasVoted = votedChatbots.includes(chatbot.id);
        const voteDisabled = hasVoted ? "disabled" : "";
        const voteClass = hasVoted ? "button-disabled" : "";

        return matchesSearch && (!favoritesOnly || isFavorite) && tagMatchesFilter;
    });

  filteredChatbots = filteredChatbots.sort((a, b) => b.rating - a.rating);

  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const chatbotsToShow = filteredChatbots.slice(startIndex, endIndex);
  console.log(`Rendering chatbots from index ${startIndex} to ${endIndex}`);

  const chatbotGrid = document.getElementById('chatbot-grid');
  chatbotGrid.innerHTML = '';

  chatbotsToShow.forEach((chatbot) => {
    let favoriteColorIndicator = favoriteChatbots.has(chatbot.id) ? favoriteColor : notFavoriteColor;
    let deleteButton = '';
    let editButton = '';
    let rating = chatbot.rating;
    let tags = chatbot.tags.map(tag => `<div class="tag-container"><span class="tag" onclick="applyTagFilter('${tag}')">#${tag}</span></div>`).join(' ');
    let voteDisabled = votedChatbots.includes(chatbot.id) ? 'disabled' : ''; 
    let voteClass = voteDisabled ? 'button-disabled' : '';

    if (userRole === 'admin') {
      editButton = `<button type="button" class="button edit-button" onclick="location.href='/chatbots/edit/${chatbot.id}'">Edit</button>`;
      deleteButton = `<button type="button" class="button delete-button" onclick="deleteChatbot(${chatbot.id})">Delete</button>`;
    }

    const chatbotCard = `
    <div class="chatbot-card" data-id="${chatbot.id}">
  
    <h3 class="chatbot-name">${chatbot.name}</h3>
    <div class="chatbot-details">
      <div class="chatbot-avatar-container">
        <img class="chatbot-avatar" src="/static/${chatbot.avatarpath}" alt="${chatbot.name}" />
        <div class="favorite-container">
        <i class="fa fa-heart favorite-icon" onclick="favoriteChatbot(${chatbot.id})" style="color:${favoriteColorIndicator};"></i>
      </div>
      </div>

        <div class="chatbot-tags">${tags}</div>
      </div>
      <div class="chatbot-voting">
        <button ${voteDisabled} class="vote-button thumbs-up ${voteClass}" onclick="vote(${chatbot.id}, 1)">
          <i class="fas fa-thumbs-up"></i>
        </button>
        <button ${voteDisabled} class="vote-button thumbs-down ${voteClass}" onclick="vote(${chatbot.id}, -1)">
          <i class="fas fa-thumbs-down"></i>
        </button>
        <div class="rating-container">
        <span class="rating-value">Rating: ${rating}</span>
      </div>
    </div>
      <div class="chatbot-actions">
        <button type="button" class="button-glass-chat" onclick="location.href='/chatroom/${chatbot.id}'">Chat</button>
        <button type="button" class="button-glass-view" onclick="location.href='/chatbots/${chatbot.id}'">View</button>
        <button type="button" class="button-glass-edit" onclick="location.href='/chatbots/edit/${chatbot.id}'">Edit</button>
        <button type="button" class="button-glass-delete" onclick="deleteChatbot(${chatbot.id})">Delete</button>
      </div>
    
  `;
  
  chatbotGrid.innerHTML += chatbotCard;
  
});
}

async function vote(chatbotId, voteChange) {
    console.log(`vote function called with chatbotId: ${chatbotId}, voteChange: ${voteChange}`);

    const votedChatbots = JSON.parse(localStorage.getItem('votedChatbots')) || [];
    if (votedChatbots.includes(chatbotId)) {
        console.log('User has already voted for this chatbot');
        return; 
    }

    let voteUrl;
    if (voteChange > 0) {
        voteUrl = `/api/chatbots/${chatbotId}/upvote`;
    } else {
        voteUrl = `/api/chatbots/${chatbotId}/downvote`;
    }

    const response = await fetch(voteUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        console.log('Vote request succeeded');
        const data = await response.json();
        console.log(`Updated rating is: ${data.rating}`);
        console.log(`Update rating in chatbotCard ${chatbotId}`);
        const chatbotCard = document.querySelector(`.chatbot-card[data-id='${chatbotId}']`);
        const ratingValueElement = chatbotCard.querySelector('.rating-value');
        ratingValueElement.innerText = data.rating;

        votedChatbots.push(chatbotId);
        localStorage.setItem('votedChatbots', JSON.stringify(votedChatbots));

        const upvoteButton = chatbotCard.querySelector(`button[onclick="vote(${chatbotId}, 1)"]`);
        const downvoteButton = chatbotCard.querySelector(`button[onclick="vote(${chatbotId}, -1)"]`);
        upvoteButton.disabled = true;
        downvoteButton.disabled = true;

        upvoteButton.classList.add('button-disabled');
        downvoteButton.classList.add('button-disabled');
    } else {
        console.log('Vote failed');
    }
}




async function favoriteChatbot(chatbotId) {
  console.log(`favoriteChatbot function called with chatbotId: ${chatbotId}`);

  const chatbotCard = document.querySelector(`.chatbot-card[data-id='${chatbotId}']`);
  const favoriteIcon = chatbotCard.querySelector('.favorite-icon');

  const method = favoriteChatbots.has(chatbotId) ? 'DELETE' : 'POST';
  const newColor = favoriteChatbots.has(chatbotId) ? notFavoriteColor : favoriteColor;

  favoriteIcon.style.color = newColor;

  console.log(`Sending ${method} request to /api/favorites for chatbot ${chatbotId}`);

  const response = await fetch('/api/favorites', {
    method: method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ chatbot_id: chatbotId })
  });

  if (response.ok) {
    console.log(`Successfully processed ${method} request for chatbot ${chatbotId}`);
    
    if (method === 'DELETE') {
      favoriteChatbots.delete(chatbotId);
    } else {
      favoriteChatbots.add(chatbotId);
    }
  } else {
    console.log(`Failed to process ${method} request for chatbot ${chatbotId}`);
    
    favoriteIcon.style.color = favoriteChatbots.has(chatbotId) ? favoriteColor : notFavoriteColor;
  }
}

function applyTagFilter(tag) {
  console.log(`applyTagFilter function called with tag: ${tag}`);

  // Toggle tag in filter
  if (tagFilter.has(tag)) {
      tagFilter.delete(tag);
  } else {
      tagFilter.add(tag);
  }

  // Update tag button styles
  updateTagButtonStyles();

  // Render active tags
  renderActiveTags();

  currentPage = 1;
  renderChatbots();
}

function updateTagButtonStyles() {
  document.querySelectorAll('.tag, .tag-button').forEach(element => {
      if (tagFilter.has(element.textContent)) {
          element.classList.add('active-tag');
      } else {
          element.classList.remove('active-tag');
      }
  });
}

function renderActiveTags() {
  const activeTagsContainer = document.querySelector('.container-active-tags');
  activeTagsContainer.innerHTML = '';

  tagFilter.forEach(tag => {
      const button = document.createElement('button');
      button.textContent = tag;
      button.classList.add('tag-button', 'active-tag');
      button.onclick = () => applyTagFilter(tag);
      activeTagsContainer.appendChild(button);
  });
}


function renderPagination() {
  console.log('renderPagination function called');

  const paginationElement = document.getElementById('pagination');
  paginationElement.innerHTML = '';

  const totalPages = Math.ceil(filteredChatbots.length / itemsPerPage);

  
  if (totalPages > 1) {
    for (let page = 1; page <= totalPages; page++) {
      const button = document.createElement('button');

      button.classList.add('button-pagination-glass');
      button.innerText = `${page}`;

      if (page === currentPage) {
        button.classList.add('active');
      }

      button.addEventListener('click', function () {
        console.log(`Pagination button ${page} clicked`);
        currentPage = page;
        renderChatbots();
        renderPagination();
      });

      paginationElement.appendChild(button);
    }
  }
}


async function deleteChatbot(id) {
  console.log(`deleteChatbot function called with id: ${id}`);

  const userConfirmed = window.confirm('Are you sure you want to delete this chatbot?');
  if (!userConfirmed) {
    return;
  }

  const response = await fetch('/chatbots/' + id + '/delete', { method: 'POST' });
  const result = await response.json();
  if (result.status === 'success') {
    currentPage = 1;
    const response = await fetch('/api/chatbots');
    chatbots = await response.json();
    renderChatbots();
    renderPagination();
  } else {
    alert(result.message);
  }
}

function setSearchFilter(newFilter) {
  console.log(`setSearchFilter function called with newFilter: ${newFilter}`);

  searchFilter = newFilter;
  currentPage = 1;
  renderChatbots();
  renderPagination();
}

function setFavoritesOnly(newFavoritesOnly) {
  console.log(`setFavoritesOnly function called with newFavoritesOnly: ${newFavoritesOnly}`);

  favoritesOnly = newFavoritesOnly;
  currentPage = 1;
  renderChatbots();
  renderPagination();
}
