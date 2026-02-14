let url= "http://127.0.0.1:8000/getjson";


document. getElementById("opcion").addEventListener("change", async function () {
    
    let localidadSeleccionada = this.value;
    let myAPI = url + "?a=" + localidadSeleccionada;
    let response = await fetch(myAPI);
    let datos= await response.json();

    console.log(datos);
});