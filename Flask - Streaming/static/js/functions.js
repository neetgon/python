function delete_video_frame(){
  var video = document.getElementById('video-content');
  video.style.width = "0px";
  video.style.height = "0px";
  video.pause();
  
  var source = document.getElementById("source");
  source.src = "";
  
  video.load();
  
  document.getElementById("player").style.display = "none";
  document.getElementsByClassName("back")[0].style.display = "none";
  
  document.body.style.overflow = "visible";
}

function insert_video_in_frame(url, sub){
  document.getElementsByClassName("back")[0].style.display = "block";
  document.getElementById("player").style.display = "block";
  document.getElementById("track-sub").src = sub;
  
  var video = document.getElementById("video-content")
  var source = document.getElementById("source");
  
  
  source.src = url;
  video.style.display = "block";
  video.load();
  video.play();
  
  video.style.transition = "2s";
  video.style.width = "100%";
  video.style.height = "100%";
  
  document.body.style.overflow = "hidden";
}

document.onkeydown = function(evt) {
  evt = evt || window.event;
  var escape = false;
  if ("key" in evt) {
      escape = (evt.key === "Escape" || evt.key === "Esc");
  } else {
      escape = (evt.keyCode === 27);
  }
  if (escape) {
    delete_video_frame();
  }
}