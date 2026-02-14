async function descargar() {

    const localidad = document.getElementById("localidad").value;

    try {
        const response = await fetch(`http://127.0.0.1:8000/localidad/${localidad}`);

        if (!response.ok) {
            throw new Error("Error en el servidor");
        }

        const blob = await response.blob();

        // Crear URL temporal
        const url = window.URL.createObjectURL(blob);

        // Crear enlace invisible
        const a = document.createElement("a");
        a.href = url;
        a.download = `arboles_${localidad}.geojson`;
        document.body.appendChild(a);
        a.click();

        // Limpiar
        a.remove();
        window.URL.revokeObjectURL(url);

        alert("Descarga completada ✅");

    } catch (error) {
        alert("Error descargando archivo ❌");
        console.error(error);
    }
}