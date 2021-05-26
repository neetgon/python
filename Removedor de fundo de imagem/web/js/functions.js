eel.expose(open_file);
function open_file() {
  eel.open_file()
}

eel.expose(convert);
function convert() {
  var tolerancia = document.getElementById("tolerancia").value
  eel.convert_list(tolerancia)
  
  document.getElementById("tol-show").innerHTML = "Tolêrancia " + String(tolerancia)
}

eel.expose(update_image);
function update_image(display){
  document.getElementById('display').src = display
}

eel.expose(salvar);
function salvar(){
  eel.salvar()
}

eel.expose(tolerancia);
function tolerancia(){
  tolerancia = int(document.getElementById('tolerancia').value);
  return tolerancia;
}