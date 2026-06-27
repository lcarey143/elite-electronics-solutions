(function () {
  'use strict';

  const config = window.EES_CONFIG || {};
  const toggle = document.getElementById('aiToggle');
  const panel = document.getElementById('aiPanel');
  const closeBtn = document.getElementById('aiClose');
  const form = document.getElementById('aiForm');
  const input = document.getElementById('aiInput');
  const messages = document.getElementById('aiMessages');
  const suggestions = document.getElementById('aiSuggestions');

  if (!toggle || !panel) return;

  const chatHistory = [];

  toggle.addEventListener('click', () => {
    panel.hidden = false;
    toggle.hidden = true;
    input.focus();
  });

  closeBtn.addEventListener('click', () => {
    panel.hidden = true;
    toggle.hidden = false;
  });

  function getCsrfToken() {
    if (config.csrfToken) return config.csrfToken;
    const cookie = document.cookie.match(/csrftoken=([^;]+)/);
    return cookie ? cookie[1] : '';
  }

  function addMessage(text, type) {
    const div = document.createElement('div');
    div.className = 'ai-msg ' + type;
    const p = document.createElement('p');
    p.textContent = text;
    p.style.whiteSpace = 'pre-line';
    div.appendChild(p);
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  function showTyping() {
    const div = document.createElement('div');
    div.className = 'ai-msg bot typing';
    div.innerHTML = '<span></span><span></span><span></span>';
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  async function respond(question) {
    addMessage(question, 'user');
    chatHistory.push({ role: 'user', content: question });

    const typing = showTyping();
    input.disabled = true;

    try {
      const response = await fetch(config.aiChatUrl || '/api/ai/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({
          message: question,
          history: chatHistory.slice(-8),
        }),
      });

      const data = await response.json();
      typing.remove();

      if (data.success && data.reply) {
        addMessage(data.reply, 'bot');
        chatHistory.push({ role: 'assistant', content: data.reply });
      } else {
        addMessage(
          data.error || 'Sorry, I could not process that request. Please try again or contact us directly.',
          'bot'
        );
      }
    } catch (err) {
      typing.remove();
      addMessage(
        'Connection error. Please check your internet and try again, or email lashardcarey@gmail.com.',
        'bot'
      );
    } finally {
      input.disabled = false;
      input.focus();
    }
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    respond(text);
  });

  suggestions.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-q]');
    if (!btn) return;
    respond(btn.dataset.q);
  });
})();
