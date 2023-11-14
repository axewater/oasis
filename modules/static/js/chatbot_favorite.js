let userRole;
let favoriteChatbots = new Set();
let chatbotId;
window.onload = async function () {
  const roleResponse = await fetch('/api/current_user_role');
  const roleData = await roleResponse.json();
  userRole = roleData.role;
  console.log('User role:', userRole);

  const favoritesResponse = await fetch('/api/favorites');
  const favorites = await favoritesResponse.json();
  favoriteChatbots = new Set(favorites.map(String)); // convert IDs to strings
  console.log('Favorites:', favorites);

  chatbotId = document.querySelector('.favorite-icon').getAttribute('data-chatbot-id');
  console.log('Chatbot ID:', chatbotId);
};

async function favoriteChatbot(iconElement) {
    const favoriteIcon = document.querySelector('.favorite-icon[data-chatbot-id="' + chatbotId + '"]');

    // Determine the request method and the new color for the heart icon
    const method = favoriteChatbots.has(chatbotId) ? 'DELETE' : 'POST';
    const newColor = favoriteChatbots.has(chatbotId) ? 'rgba(0, 0, 0, 0.5)' : 'rgba(255, 105, 97, 1)';

    // Immediately update the heart icon color on the client side
    favoriteIcon.style.color = newColor;

    console.log(`Sending ${method} request to /api/favorites for chatbot ${chatbotId}`);

    const response = await fetch('/api/favorites', {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({chatbot_id: chatbotId})
    });

    if (response.ok) {
        console.log(`Successfully processed ${method} request for chatbot ${chatbotId}`);
        // Update the local state to reflect the new favorite status
        if (method === 'DELETE') {
            favoriteChatbots.delete(chatbotId);
        } else {
            favoriteChatbots.add(chatbotId);
        }
    } else {
        console.log(`Failed to process ${method} request for chatbot ${chatbotId}`);
        // If the request failed, revert the heart icon color to its previous state
        favoriteIcon.style.color = favoriteChatbots.has(chatbotId) ? 'rgba(255, 105, 97, 1)' : 'rgba(0, 0, 0, 0.5)';
    }
}
