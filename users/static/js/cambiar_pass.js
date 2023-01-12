    var modalWrap = null;
    const cambiarPass = (username) => {
        if (modalWrap !== null) {
            modalWrap.remove();
        }

        const csrftoken = token.innerHTML;

        modalWrap = document.createElement('div');
        modalWrap.innerHTML = `
            <div class="modal" tabindex="-1">
                <div class="modal-dialog">
                    <form method="post">
                        ${csrftoken}
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Cambiar contraseña</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body p-5">
                            
                                <div class="w-100 me-1">
                                    <div class="input-group mb-1">
                                        <input type="password" name="password1" class="form-control" id="floatingPassword1"
                                            placeholder="Nueva contraseña"
                                            aria-describedby="basic-addon1" style="height: 55px" required>
                                        <span class="input-group-text" id="basic-addon1"> <span
                                            class="material-symbols-rounded cursor" id="visible_pass">visibility</span></span>
                                    </div>
                                    <p id="messagePassword1" class="mb-4 text-start fw-lighter"></p>
                                </div>
                
                                <div class="w-100 ms-1">
                                    <div class="input-group mb-1">
                                        <input type="password" name="password2" class="form-control" id="floatingPassword2"
                                            placeholder="Repetir contraseña"
                                            aria-describedby="basic-addon2" style="height: 55px" required>
                                        <span class="input-group-text" id="basic-addon2"> <span
                                            class="material-symbols-rounded cursor" id="visible_pass2">visibility</span></span>
                                    </div>
                                    <p id="messagePassword2" class="mb-4 text-danger text-start fw-lighter"></p>
                                </div>

                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                <button type="submit" class="btn btn-primary">Cambiar contraseña</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        `;

        document.body.append(modalWrap);

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

        var modal = new bootstrap.Modal(modalWrap.querySelector('.modal'));
        modal.show();
    };

    