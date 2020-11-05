  const open = document.querySelector("#open");
  const close = document.querySelector("#close");
  const g_menu = document.querySelector("#g_menu");
  
  //メニューを出す
  open.addEventListener('click', function() {
      g_menu.classList.add('inside');
      g_menu.classList.remove('outside');
   }, false);
  
  //メニューを隠す
  close.addEventListener('click', function() {
      g_menu.classList.remove('inside');
      g_menu.classList.add('outside');
   }, false);  