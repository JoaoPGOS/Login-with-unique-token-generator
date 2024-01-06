function generateToken(length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%';
    let token = '';
    for (let i = 0; i < length; i++) {
        token += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return token;
}
function sendtoken(){
    // Gerar um token de 72 caracteres
    const token = generateToken(72);

    // Endpoint da requisição
    const endpoint = '/secondverification';

    // Dados para enviar na requisição
    const requestData = {
        token: token,
        user: document.getElementById('user').value.toUpperCase()
        // Outros dados, se necessário
    };

    // Criar a requisição XMLHTTP
    const xhr = new XMLHttpRequest();
    xhr.open('POST', endpoint, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Tratar a resposta da requisição
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            // Sucesso na requisição
            const response = JSON.parse(xhr.responseText);
            if(response['status']){
                alert(response['status']);
            }else{
            localStorage.setItem('respostaRequisicao', JSON.stringify(response));
            window.location.reload();
            }

        } else {
            // Erro na requisição
            console.error('Erro na requisição:', xhr.statusText);
        }
    };

    // Enviar a requisição com os dados JSON
    xhr.send(JSON.stringify(requestData));
}

function login(){
    const respostaArmazenada = localStorage.getItem('respostaRequisicao');


    const respostaObjeto = JSON.parse(respostaArmazenada);

    verified_user = respostaObjeto['user']
    verified_token = respostaObjeto['token']

    const verified_endpoint = '/verification';

    // Dados para enviar na requisição
    const verified_data = {
        token: verified_token,
        user: verified_user
        // Outros dados, se necessário
    };

    // Criar a requisição XMLHTTP
    const xhr = new XMLHttpRequest();
    xhr.open('POST', verified_endpoint, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Tratar a resposta da requisição
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            // Sucesso na requisição
            const response = JSON.parse(xhr.responseText);
            if(response['status'] == 'verified'){
                window.location.replace('http://127.0.0.1:5000/home')
            }
        } else {
            // Erro na requisição
            console.error('Erro na requisição:', xhr.statusText);
        }
    };

    // Enviar a requisição com os dados JSON
    xhr.send(JSON.stringify(verified_data));
}

login()
