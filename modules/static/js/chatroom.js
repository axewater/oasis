var synth = window.speechSynthesis;
var user_role = sessionStorage.getItem("user_role");
var chatbot_detail_url = sessionStorage.getItem("chatbot_detail_url");
var chatbot_edit_url = sessionStorage.getItem("chatbot_edit_url");
var avatar_html = sessionStorage.getItem("avatar_html");
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
var chunkCounter = 0;
var isNewAIResponse = true;
let isFirstChunk = true;
const CHUNK_THRESHOLD = 25;


var thread_id = sessionStorage.getItem('thread_id');
if (!thread_id) {
    thread_id = null;
}

console.log("Loading thread_id: ", thread_id);
previousMessages.sort(function(a, b) {
    return a.order - b.order;
});
for (var i = 0; i < previousMessages.length; i++) {
    var message = previousMessages[i];
    message.content = decodeHTML(message.content);
    var type = message.role === 'ai' ? 'ai' : 'user';
    add_message_to_chat(type, message.content);
}

function scrollToBottomOfChat() {
    console.log("Scrolling to bottom of chat...");
    window.scroll({
        top: document.body.scrollHeight,
        left: 0,
        behavior: "smooth",
    });
}



function countTokens(text) {

    const words = text.split(/\s+|[.,!?;:()"'-]/).filter(Boolean);
    let tokenCount = 0;
   
    words.forEach(word => {
        if (word.length <= 3) {
            tokenCount += 1;
        } else {
            tokenCount += Math.ceil(word.length / 4);
        }
    });

    return tokenCount;
}
    

function updateTokenCountDisplay() {
    var user_message = $('#user-message').val();
    var token_count = countTokens(user_message);
    var tokenDisplay = `(approx. ${token_count} of ${MAX_TOKENS} tokens used)`;
    if (token_count > MAX_TOKENS) {
        tokenDisplay = `<span style="color: red;">${tokenDisplay}</span>`;
    }
    $('#token-counter').html(tokenDisplay);
}



function sanitizeHTML(str) {
    if (str.includes('&amp;')) {
        return str;
    } else {
        var temp = document.createElement('div');
        temp.textContent = str;
        let sanitizedStr = temp.innerHTML;
        return sanitizedStr.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
    }
}


function decodeHTML(html) {
    const textArea = document.createElement('textarea');
    textArea.innerHTML = html;
    return textArea.value;
}



$('body').on('click', '.copy-code-button', function() {
    var codeContent = $(this).parent().next().find('code').text();
    var tempTextArea = document.createElement('textarea');
    tempTextArea.value = codeContent;
    document.body.appendChild(tempTextArea);
    tempTextArea.select();
    document.execCommand('copy');
    document.body.removeChild(tempTextArea);

    var originalText = $(this).text();
    $(this).text('Copied');
    var button = $(this);
    setTimeout(function() {
        button.text(originalText);
    }, 2000);
});


function clearChat() {
  var thread_id = sessionStorage.getItem('thread_id');

  var confirmClear = confirm('Are you sure you want to clear the chat?');

  if (confirmClear) {
    fetch('/delete_thread', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ thread_id: thread_id })
    })
    .then(response => {
      if (response.ok) {
        location.reload();
      } else {
        alert('Failed to clear chat');
      }
    })
    .catch(error => {
      alert('An error occurred');
      console.error(error);
    });
  }
}





function add_message_to_chat(type, message, isPartial = false) {
    // console.log(`Adding message to chat. Type: ${type}, Message: ${message}`);
    var message_class = type === 'ai' ? 'ai' : 'user';
    var speech_bubble_class = type === 'ai' ? 'speech-bubble ai' : 'speech-bubble user';
    var sanitizedMessage = sanitizeHTML(message);
    var formattedMessage = sanitizedMessage;
    
    if (type === 'ai') {
        var regex = /```([\s\S]+?)```/gs;
        formattedMessage = sanitizedMessage.replace(regex, function(match, codeContent) {
            var lines = codeContent.split('\n');
            var language = lines[0].toUpperCase();
            lines.shift();
            var code = lines.join('\n');

            return `<div class="codeblockz"><div class="title-codeblock">Language: ${language}<button class="copy-code-button">Copy</button></div><div class="formatted-code"><pre><code class="language-python">${code}</code></pre></div></div>`;
        });
    }

    $('.chatroom-messages-glass').append(`
        <div class="${message_class}">
            <div class="${speech_bubble_class}" data-partial="${isPartial}">
                <div class="container-chat-avatar-user">
                    ${type === 'user' ? `<img class="avatar" src="${avatarpath_thumbnail}" alt="User Avatar">` : ''}
                </div>
                <div class="container-chat-avatar-ai">
                    ${type === 'ai' ? avatar_html : ''}
                </div>
                <div class="formatted-message">
                    ${formattedMessage}
                </div>
            </div>
        </div>
    `);

    setTimeout(function() {
        $('.chatroom-messages-glass').scrollTop($('.chatroom-messages-glass')[0].scrollHeight);
    }, 10);

    if (type == 'ai') {
        Prism.highlightAll();
    }

    
}


$('#chat-form').submit(function(event) {
    event.preventDefault();
    var user_message = $('#user-message').val().trim();
    var token_count = countTokens(user_message);

    if (user_message.length === 0) {
        console.log('User message is empty. Ignoring submission.');
        return;
    }

    if (token_count > MAX_TOKENS) {
        console.log(`User message exceeds token limit. Token count: ${token_count}, Max tokens: ${MAX_TOKENS}`);
        alert(`Your message is too long (${token_count} tokens). It should be less than ${MAX_TOKENS} tokens.`);
        return;
    }

    console.log("Submitting user message: ", user_message);
    add_message_to_chat('user', user_message);
    $('#user-message').val('');
    isNewAIResponse = true;

    console.log("Emitting start_chat event with message: ", user_message);
    socket.emit('start_chat', {
        message: user_message,
        bot_id: bot_id,
        thread_id: thread_id
    });
});

$(document).ready(function() {
    $('#user-message').on('input', function () {
      this.style.height = 'auto';
      this.style.height = (this.scrollHeight) + 'px';
      var screenHeight = $(window).height();
      var maxHeight = screenHeight * 0.5;
      if (parseInt(this.style.height) > maxHeight) {
        this.style.height = maxHeight + 'px';
        this.scrollTop = this.scrollHeight;
      }
      updateTokenCountDisplay();
    });
    updateTokenCountDisplay();
  });


socket.on('connect', function() {
    console.log('Oasis socket connected!');
});

socket.on('chat_response', function(data) {
    
    if (isFirstChunk && !data.message.trim()) {
        console.log("Received an empty first chunk, ignoring it.");
        isFirstChunk = false; 
        return;
    }
    
    
    chunkCounter++;
    console.log("Chat chunk count: ", chunkCounter);
    
    var currentContent = $('.ai:last .formatted-message').html();
    console.log("Current content: ", currentContent);
    var newContent = data.message ? sanitizeHTML(currentContent + data.message) : currentContent;
    
    $('.ai:last .formatted-message').html(newContent);
    console.log("New content: ", newContent);
    if (data.final_chunk) {
        console.log('End chunk detected!');
        $('.ai:last .formatted-message').data('partial', false);
        console.log("Partial status: ", $('.ai:last .formatted-message').data('partial'));
        scrollToBottomOfChat();
        isNewAIResponse = true;
        isFirstChunk = false;
    } else {
        console.log("Partial status: ", $('.ai:last .formatted-message').data('partial'));
        $('.ai:last .formatted-message').data('partial', true);
    }

    if (chunkCounter >= CHUNK_THRESHOLD) {
        console.log("Exceeding chunk threshold, reapplying Prism! chunk#", chunkCounter);
        Prism.highlightElement($('.ai:last .formatted-message')[0]);
        chunkCounter = 0;
        scrollToBottomOfChat();
    }

    if (isNewAIResponse && data.message) {
        console.log("Creating new AI bubble");
        add_message_to_chat('ai', data.message, true);
        isNewAIResponse = false;
    }
});

scrollToBottomOfChat();