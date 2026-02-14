let url= "http://127.0.0.1:8000/getjson";


async function crearPeticion(){
    let myAPI = url + "?"
    let response = await fetch(myAPI);
    let datos= await response.json();

    console.log(datos);
}