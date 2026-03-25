(function() {
  var CHAT_ENDPOINT = 'https://n8n.myaibuffet.com/webhook/stromation-chat';
  var history = [];
  var isOpen = false;
  var isLoading = false;

  // Build the widget HTML
  var widget = document.createElement('div');
  widget.id = 'strom-chat';
  widget.innerHTML =
    '<button id="strom-chat-toggle" aria-label="Open chat">' +
      '<svg id="strom-toggle-open" xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 24 24">' +
        '<path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12zM7 9h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/>' +
      '</svg>' +
      '<svg id="strom-toggle-close" xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="display:none">' +
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>' +
      '</svg>' +
      '<div id="strom-chat-badge"></div>' +
    '</button>' +
    '<div id="strom-chat-bubble">Chat with us<div class="strom-bubble-arrow"></div></div>' +
    '<div id="strom-chat-window">' +
      '<div id="strom-chat-header">' +
        '<div style="display:flex;align-items:center;gap:0.75rem">' +
          '<div style="position:relative">' +
            '<img id="strom-header-avatar" src="logo.svg" alt="Stromation" style="width:32px;height:32px;" />' +
            '<div id="strom-chat-status"></div>' +
          '</div>' +
          '<div>' +
            '<strong style="font-size:0.95rem">Darius</strong>' +
            '<div style="font-size:0.7rem;opacity:0.8">Founder, Stromation</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div id="strom-chat-messages"></div>' +
      '<form id="strom-chat-form">' +
        '<input id="strom-chat-input" type="text" placeholder="Type a message..." autocomplete="off" />' +
        '<button type="submit" id="strom-chat-send" aria-label="Send">' +
          '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">' +
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>' +
          '</svg>' +
        '</button>' +
      '</form>' +
    '</div>';

  document.body.appendChild(widget);

  var toggle = document.getElementById('strom-chat-toggle');
  var chatWindow = document.getElementById('strom-chat-window');
  var messagesDiv = document.getElementById('strom-chat-messages');
  var form = document.getElementById('strom-chat-form');
  var input = document.getElementById('strom-chat-input');
  var toggleOpen = document.getElementById('strom-toggle-open');
  var toggleClose = document.getElementById('strom-toggle-close');
  var badge = document.getElementById('strom-chat-badge');
  var isSubpage = window.location.pathname.indexOf('/blog/') !== -1;
  if (isSubpage) {
    document.getElementById('strom-header-avatar').src = '../logo.svg';
  }

  var bubble = document.getElementById('strom-chat-bubble');

  // Show welcome after a short delay
  setTimeout(function() {
    addBotMessage('Hey! I\'m Darius, founder of Stromation. Got questions about automating your workflows? Fire away.');
    badge.classList.add('strom-badge-show');
    bubble.classList.add('strom-bubble-show');
  }, 2000);

  // Dismiss bubble on click
  bubble.addEventListener('click', function() {
    toggle.click();
  });

  toggle.addEventListener('click', function() {
    isOpen = !isOpen;
    chatWindow.classList.toggle('strom-chat-open', isOpen);
    toggle.classList.toggle('strom-chat-active', isOpen);
    toggleOpen.style.display = isOpen ? 'none' : 'block';
    toggleClose.style.display = isOpen ? 'block' : 'none';
    badge.classList.remove('strom-badge-show');
    bubble.classList.remove('strom-bubble-show');
    if (isOpen) input.focus();
  });

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var msg = input.value.trim();
    if (!msg || isLoading) return;

    addUserMessage(msg);
    history.push({ role: 'user', content: msg });
    input.value = '';
    isLoading = true;

    // Show typing indicator
    var typingEl = document.createElement('div');
    typingEl.className = 'strom-msg-row strom-typing-row';
    typingEl.innerHTML =
      '<img src="' + (isSubpage ? '../' : '') + 'logo.svg" alt="" class="strom-avatar" />' +
      '<div class="strom-msg strom-msg-bot strom-typing"><span></span><span></span><span></span></div>';
    messagesDiv.appendChild(typingEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    fetch(CHAT_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, history: history })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      typingEl.remove();
      var reply = data.reply || 'Sorry, something went wrong. Try again or email support@stromation.com.';
      addBotMessage(reply);
      history.push({ role: 'assistant', content: reply });
    })
    .catch(function() {
      typingEl.remove();
      addBotMessage('Hmm, connection issue on my end. Email me at support@stromation.com or text (855) 932-0493 and I\'ll get right back to you.');
    })
    .finally(function() {
      isLoading = false;
    });
  });

  function addBotMessage(text) {
    var row = document.createElement('div');
    row.className = 'strom-msg-row';
    var avatar = document.createElement('img');
    avatar.src = (isSubpage ? '../' : '') + 'logo.svg';
    avatar.alt = '';
    avatar.className = 'strom-avatar';
    var bubble = document.createElement('div');
    bubble.className = 'strom-msg strom-msg-bot';
    bubble.textContent = text;
    row.appendChild(avatar);
    row.appendChild(bubble);
    messagesDiv.appendChild(row);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  function addUserMessage(text) {
    var div = document.createElement('div');
    div.className = 'strom-msg strom-msg-user';
    div.textContent = text;
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }
})();
