visible_pass.addEventListener("click", () => {
    if (visible_pass.innerHTML == "visibility") {
        visible_pass.innerHTML = "visibility_off";
        floatingPassword1.type = "text";
    } else {
        visible_pass.innerHTML = "visibility";
        floatingPassword1.type = "password";
    }
});

visible_pass2.addEventListener("click", () => {
    if (visible_pass2.innerHTML == "visibility") {
        visible_pass2.innerHTML = "visibility_off";
        floatingPassword2.type = "text";
    } else {
        visible_pass2.innerHTML = "visibility";
        floatingPassword2.type = "password";
    }
});

floatingInput.addEventListener("input", ()=>{
    if(floatingInput.value == ""){
        floatingInput.classList.add("invalid-form");
        messageUser.classList.add("text-danger");
        messageUser.innerHTML = "Introduzca un nombre de usuario";
    }else{
        floatingInput.classList.remove("invalid-form");
        messageUser.classList.remove("text-danger");
        messageUser.innerHTML = "";
    }
});

floatingEmail.addEventListener("input", ()=>{
    if(floatingEmail.value == ""){
        floatingEmail.classList.add("invalid-form");
        messageEmail.classList.add("text-danger");
        messageEmail.innerHTML = "Introduzca un correo electrónico";
    }else{
        floatingEmail.classList.remove("invalid-form");
        messageEmail.classList.remove("text-danger");
        messageEmail.innerHTML = "";
    }
});

floatingNombre.addEventListener("input", ()=>{
    if(floatingNombre.value == ""){
        floatingNombre.classList.add("invalid-form");
        messageNombre.classList.add("text-danger");
        messageNombre.innerHTML = "Introduzca su nombre";
    }else{
        floatingNombre.classList.remove("invalid-form");
        messageNombre.classList.remove("text-danger");
        messageNombre.innerHTML = "";
    }
});

floatingApellidos.addEventListener("input", ()=>{
    if(floatingApellidos.value == ""){
        floatingApellidos.classList.add("invalid-form");
        messageApellidos.classList.add("text-danger");
        messageApellidos.innerHTML = "Introduzca sus apellidos";
    }else{
        floatingApellidos.classList.remove("invalid-form");
        messageApellidos.classList.remove("text-danger");
        messageApellidos.innerHTML = "";
    }
});

floatingPassword1.addEventListener("input", ()=>{
    if(floatingPassword1.value.length < 8){
        floatingPassword1.classList.remove("correct-form");
        floatingPassword1.classList.add("invalid-form");
        messagePassword1.classList.add("text-danger");
        messagePassword1.innerHTML = "Su contraseña debe tener mínimo 8 carácteres";
    }else{
        floatingPassword1.classList.remove("invalid-form");
        floatingPassword1.classList.add("correct-form");
        messagePassword1.classList.remove("text-danger");
        messagePassword1.classList.add("text-success");
        messagePassword1.innerHTML = "Contraseña aceptable";
    }
});

floatingPassword2.addEventListener("input", ()=>{
    if(floatingPassword1.value != floatingPassword2.value){
        floatingPassword2.classList.add("invalid-form");
        messagePassword2.classList.add("text-danger");
        messagePassword2.innerHTML = "Las contraseñas no coinciden";
    }else{
        floatingPassword2.classList.remove("invalid-form");
        messagePassword2.classList.remove("text-danger");
        messagePassword2.innerHTML = "";
    }
});

selectPais.addEventListener("change", ()=>{
    if(selectPais.value != ""){
        selectPais.classList.remove("invalid-form");
    }
});

enviar_formlario = () =>{   
    if(floatingPassword1.value.length >= 8 && floatingPassword1.value == floatingPassword2.value && floatingInput.value != "" && floatingEmail.value != "" && floatingNombre.value != "" && floatingApellidos.value != "" && selectPais.value != ""){
        document.formulario.submit();
    }

    if(floatingInput.value == ""){
        floatingInput.classList.add("invalid-form");
        messageUser.classList.add("text-danger");
        messageUser.innerHTML = "Introduzca un nombre de usuario";
    }

    if(floatingNombre.value == ""){
        floatingNombre.classList.add("invalid-form");
        messageNombre.classList.add("text-danger");
        messageNombre.innerHTML = "Introduzca su nombre";
    }

    if(floatingApellidos.value == ""){
        floatingApellidos.classList.add("invalid-form");
        messageApellidos.classList.add("text-danger");
        messageApellidos.innerHTML = "Introduzca sus apellidos";
    }

    if(selectPais.value == ""){
        selectPais.classList.add("invalid-form");
    }

    if(floatingEmail.value == ""){
        floatingEmail.classList.add("invalid-form");
        messageEmail.classList.add("text-danger");
        messageEmail.innerHTML = "Introduzca un correo electrónico";
    }

    if(floatingPassword1.value.length < 8){
        floatingPassword1.classList.add("invalid-form");
        messagePassword1.classList.add("text-danger");
        messagePassword1.innerHTML = "Su contraseña debe tener mínimo 8 carácteres";
    }

    if(floatingPassword1.value != floatingPassword2.value){
        floatingPassword2.classList.add("invalid-form");
        messagePassword2.classList.add("text-danger");
        messagePassword2.innerHTML = "Las contraseñas no coinciden";
    }

};