    var MAX_TOKENS = 3800;
    var synth = window.speechSynthesis;
    var user_role = sessionStorage.getItem("user_role");
    var chatbot_detail_url = sessionStorage.getItem("chatbot_detail_url");
    var chatbot_edit_url = sessionStorage.getItem("chatbot_edit_url");
    var avatar_html = sessionStorage.getItem("avatar_html");

let firstTimeout;
let secondTimeout;


    window.speechSynthesis.onvoiceschanged = function() {
        console.log("All available voices: ", window.speechSynthesis.getVoices());
    };
    function speak(text) {
        if (!speech_enabled) {
            return;
        }
        switch (tts_engine) {
        case 'amazon':
            // amazon TTS API code
            break;
        case 'google':
            // google TTS API code
            break;
        case 'azure':
            // Microsoft Azure TTS API code
            break;
        case 'elevenlabs':
            // elevenlabs TTS API code
            break;
        default:
            console.log("Triggering webspeech now");
            var utterThis = new SpeechSynthesisUtterance(text);
            var voices = synth.getVoices();
            for(i = 0; i < voices.length ; i++) {
                if((voicetype == "male" && voices[i].name.includes("Male")) || (voicetype == "female" && voices[i].name.includes("Female"))) {
                    utterThis.voice = voices[i];
                    break;
                }
            }
            synth.speak(utterThis);
        }
    }


    // Load previous messages
    var thread_id = sessionStorage.getItem('thread_id');
    if (!thread_id) {
        thread_id = null;
    }
    console.log("Current thread_id: ", thread_id);
    // Sort the messages by order before processing them
    previousMessages.sort(function(a, b) {
        return a.order - b.order;
    });
    for (var i = 0; i < previousMessages.length; i++) {
        var message = previousMessages[i];
        var type = message.role === 'ai' ? 'ai' : 'user';
        add_message_to_chat(type, message.content);
    }

function countTokens(text) {
    var token_count = Math.floor(text.length / 4);
    return token_count;
}

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
  });
});

function add_message_to_chat(type, message) {
    var message_class = type === 'ai' ? 'ai' : 'user';
    var speech_bubble_class = type === 'ai' ? 'speech-bubble ai' : 'speech-bubble user';
    var sanitizedMessage = sanitizeHTML(message);

    var formattedMessage = sanitizedMessage;
    if (type === 'ai') {
        var regex = /```([\s\S]+?)```/gs; // g for global, s for multiline match
        formattedMessage = sanitizedMessage.replace(regex, function(match, codeContent) {
            // Split the content by new lines
            var lines = codeContent.split('\n');
            // Extract the language from the first line and remove it
            var language = lines[0].toUpperCase();  // Here is the change
            lines.shift();
            // Join the lines back together for the actual code
            var code = lines.join('\n');

            // Return the modified HTML including the language name and 'copy code' button
            return `<div class="codeblockz"><div class="title-codeblock">Language: ${language}<button class="copy-code-button">Copy</button></div><div class="formatted-code"><pre><code class="language-python">${code}</code></pre></div></div>`;
        });
    }



    $('.chatroom-messages-glass').append(`
        <div class="${message_class}">
            <div class="${speech_bubble_class}">
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

    // Reapply Prism's formatting
    if (type === 'ai') {
        Prism.highlightAll();
    }

    window.scroll({
      top: document.body.scrollHeight,
      left: 0,
      behavior: "smooth",
    });
}

// Use jQuery's on method to ensure dynamically added buttons also have the event listener
$('body').on('click', '.copy-code-button', function() {
    // Get the code content
    var codeContent = $(this).parent().next().find('code').text();
    // Create a temporary textarea to copy the content
    var tempTextArea = document.createElement('textarea');
    tempTextArea.value = codeContent;
    document.body.appendChild(tempTextArea);
    tempTextArea.select();
    document.execCommand('copy');
    document.body.removeChild(tempTextArea);

    // Give a visual feedback (Change the button text temporarily)
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


function sanitizeHTML(str) {
    var temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
};


    $('#chat-form').submit(function(event) {
        event.preventDefault();
        var user_message = $('#user-message').val().trim();
        var token_count = countTokens(user_message);

        if (user_message.length === 0) {
            return;
        }

        if (token_count > MAX_TOKENS) {
            alert(`Your message is too long (${token_count} tokens). It should be less than ${MAX_TOKENS} tokens.`);
            return;
        }

        add_message_to_chat('user', user_message);
        $('#user-message').val('');
        console.log("Sending thread_id: ", thread_id);
          // Setting the initial timeout to display the message after 30 seconds.
        firstTimeout = setTimeout(function() {
           $('.chatroom-messages-glass').append('<p id="waiting-text">Processing is taking longer than expected. Please wait...</p>');

        // Setting the second timeout to handle it as an error if no response after another 30 seconds.
        secondTimeout = setTimeout(function() {
            console.error("Request took too long.");
            alert("Request took too long. Please try again.");
            // You can reload the page or handle this in any other way.
            location.reload();
        }, 30000);
    }, 90000);
        $('.spinner').show();

        $.ajax({
            type: "POST",
            url: '/api/chat',
            data: {
                message: user_message,
                bot_id: bot_id,
                thread_id: thread_id
            },
            timeout: 120000,  // 60 seconds timeout
            success: function(data) {
                clearTimeout(firstTimeout);
                clearTimeout(secondTimeout);
                $('#waiting-text').remove(); // Remove the waiting text if it exists.
                 if (data.error) {
                    console.log("API returned error: ", data.error);
                    alert(data.error);
                } else {
                    thread_id = data.thread_id;
                    sessionStorage.setItem('thread_id', thread_id);
                    console.log("Received thread_id from API: ", thread_id);
                    add_message_to_chat('ai', data.response);
                    speak(data.response);
                }
            },
           error: function (jqXHR, textStatus, errorThrown) {
                clearTimeout(firstTimeout);
                clearTimeout(secondTimeout);
                $('#waiting-text').remove(); // Remove the waiting text if it exists.

                if (textStatus === "timeout") {
                    console.error("Request timed out.");
                    alert("Request took too long. Please try again.");
                    location.reload();
                } else {
                    console.error("Request failed: ", textStatus, ", ", errorThrown);
                    alert("Request failed: " + textStatus);
                }
            },
            complete: function() {
                $('.spinner').hide();
                console.log("Request completed.");
            }
        });
    });
