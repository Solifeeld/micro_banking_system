// Verificação para o formulário de login
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const loginEmail = document.getElementById('loginEmail').value;
        const loginPassword = document.getElementById('loginPassword').value;

        const form = document.getElementById('loginForm');
        form.submit(); // Submete o formulário ao backend para autenticação

    });

    document.getElementById('registerBtn').addEventListener('click', function() {
        window.location.href = "/register";
    });
}

// Verificação para o formulário de registro
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', function(event) {
        // Obter valores dos campos do formulário
        const registerEmail = document.getElementById('registerEmail').value;
        
        // Verificação se o email já existe no "banco de dados"
        const emailExists = users.some(function(user) {
            return user.email === registerEmail;
        });

        if (emailExists) {
            alert('O email informado já está registrado. Por favor, use outro email.');
            event.preventDefault(); // Impede o envio do formulário se o email já existir
            return;
        }

        // Outras validações...
    });
}


// Função de Logout
if (document.getElementById('logoutBtn')) {
    document.getElementById('logoutBtn').addEventListener('click', function(event) {
        event.preventDefault(); // Impede o comportamento padrão do link
        fetch('/logout', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    window.location.href = "/";
                } else {
                    alert("Erro ao tentar fazer logout. Tente novamente.");
                }
            })
            .catch(error => console.error('Erro:', error));
    });
}


// Verificação para o formulário de login
// ... (outros scripts existentes)

// Verifique se o botão de Home está presente na página
if (document.querySelector('.home-icon a')) {
    document.querySelector('.home-icon a').addEventListener('click', function(event) {
        event.preventDefault(); // Impede o comportamento padrão do link
        window.location.href = "/home"; // Redireciona para /home
    });
}

// Verifica se o ícone de retorno está presente na página
if (document.querySelector('.return-icon a')) {
    document.querySelector('.return-icon a').addEventListener('click', function(event) {
        event.preventDefault(); // Impede o comportamento padrão do link
        window.location.href = "/"; // Redireciona para /index
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const clearBtn = document.getElementById('clearBtn');
    
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            console.log('Botão Limpar clicado');
            
            // Verifica em qual página estamos
            if (document.body.classList.contains('transferencia')) {
                document.getElementById('destinationAccount').value = '';
                document.getElementById('transferValue').value = '';
            } else if (document.body.classList.contains('saque')) {
                document.getElementById('withdrawValue').value = '';
            } else if (document.body.classList.contains('deposito')) {
                document.getElementById('depositValue').value = '';
            }
        });
    }
});

// Listener para o botão transferir
document.addEventListener('DOMContentLoaded', function() {
    const transferBtn = document.getElementById('transferBtn');

    if (transferBtn) {
        transferBtn.addEventListener('click', function() {
            const destinationAccount = document.getElementById('destinationAccount').value;
            const transferValue = parseFloat(document.getElementById('transferValue').value);

            if (transferValue > 0 && destinationAccount) {
                console.log('Iniciando a transferência...'); // Log para depuração
                fetch('/transferencia', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ destinationAccount, amount: transferValue })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Transferência realizada com sucesso!');
                        window.location.href = "/transferencia";
                    } else {
                        alert('Erro ao realizar transferência: ' + data.message);
                    }
                })
                .catch(error => console.error('Erro:', error));
            } else {
                alert('Por favor, insira um valor válido e uma conta de destino.');
            }
        });
    } else {
        console.error('Elemento transferBtn não encontrado na página.');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const withdrawBtn = document.getElementById('withdrawBtn');

    if (withdrawBtn) {
        console.log('Botão Sacar encontrado e evento atribuído.');
        withdrawBtn.addEventListener('click', function() {
            const withdrawValue = parseFloat(document.getElementById('withdrawValue').value);

            if (withdrawValue > 0) {
                console.log('Iniciando saque...'); // Log para depuração
                fetch('/saque', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ amount: withdrawValue })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Saque realizado com sucesso!');
                        window.location.href = "/saque";
                    } else {
                        alert('Erro ao realizar saque: ' + data.message);
                    }
                })
                .catch(error => console.error('Erro:', error));
            } else {
                alert('Por favor, insira um valor válido para o saque.');
            }
        });
    } else {
        console.error('Botão Sacar não encontrado.');
    }
});


// Funcionalidade de depósito
document.getElementById('depositBtn').addEventListener('click', function() {
    window.location.href = "/deposito";
});

// Funcionalidade de depósito
document.getElementById('depositBtn').addEventListener('click', function() {
    const depositValue = parseFloat(document.getElementById('depositValue').value);

    if (depositValue > 0) {
        fetch('/deposito', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount: depositValue })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Depósito realizado com sucesso!');
                window.location.href = "/deposito";
            } else {
                alert('Erro ao realizar depósito: ' + data.message);
            }
        })
        .catch(error => console.error('Erro:', error));
    } else {
        alert('Por favor, insira um valor válido para o depósito.');
    }
});

// Funcionalidade de saque
document.getElementById('withdrawBtn').addEventListener('click', function() {
    window.location.href = "/saque";
});

// Funcionalidade de transferência
document.getElementById('transferBtn').addEventListener('click', function() {
    window.location.href = "/transferencia";
});

