(function(){
  'use strict';
  var lb = document.querySelector('.tm-lb');
  if (!lb) return;
  var stage = lb.querySelector('.tm-lb-stage');
  var title = lb.querySelector('.tm-lb-title');
  var story = lb.querySelector('.tm-lb-story');
  var closeBtn = lb.querySelector('.tm-lb-close');
  var lastFocus = null;

  function clearStage(){
    stage.innerHTML = '';
  }
  function openMemory(card){
    var kind = card.getAttribute('data-kind');
    var name = card.getAttribute('data-name') || '';
    var cap = card.getAttribute('data-caption') || '';
    lastFocus = document.activeElement;
    clearStage();
    if (kind === 'video'){
      var v = document.createElement('video');
      v.setAttribute('controls','');
      v.setAttribute('playsinline','');
      v.setAttribute('preload','metadata');
      v.poster = card.getAttribute('data-poster');
      var s = document.createElement('source');
      s.src = card.getAttribute('data-src');
      s.type = 'video/mp4';
      v.appendChild(s);
      stage.appendChild(v);
    } else {
      var pic = document.createElement('picture');
      var src = document.createElement('source');
      src.type = 'image/webp';
      src.srcset = card.getAttribute('data-webp');
      var img = document.createElement('img');
      img.src = card.getAttribute('data-jpg');
      img.alt = card.getAttribute('data-alt') || '';
      img.decoding = 'async';
      pic.appendChild(src);
      pic.appendChild(img);
      stage.appendChild(pic);
    }
    title.textContent = name;
    story.textContent = cap;
    lb.hidden = false;
    lb.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }
  function closeLb(){
    var playing = stage.querySelector('video');
    if (playing){ try{ playing.pause(); }catch(e){} }
    clearStage();
    lb.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.querySelectorAll('.tm-card').forEach(function(card){
    card.addEventListener('keydown', function(e){
      if (e.target.closest('.tm-play')) return;
      if (e.key==='Enter' || e.key===' '){ e.preventDefault(); openMemory(card); }
    });
    card.addEventListener('click', function(e){
      var play = e.target.closest('.tm-play');
      if (play){
        e.preventDefault();
        e.stopPropagation();
        var video = card.querySelector('video');
        if (!video) return;
        card.classList.add('is-playing');
        video.setAttribute('controls','');
        video.play();
        return;
      }
      e.preventDefault();
      openMemory(card);
    });
  });

  closeBtn.addEventListener('click', closeLb);
  lb.addEventListener('click', function(e){ if (e.target === lb) closeLb(); });
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' && !lb.hidden) closeLb();
  });
})();
