const params = new URLSearchParams(window.location.search);
const game = params.get('game');
const content = document.getElementById('content');
if (game) {
    document.getElementById('title').innerText = `gameatlas@${game}`;
    if(game === 'albiononline'){albiononline();}
}

function albiononline(){
    fetch('../data/mmorpg/albiononline.json')
    .then(response => response.json())
    .then(data => {
        document.title = `gameatlas@${data['title']}`;
        content.innerHTML += `<h1>${data['title']}</h1>`;
    });
}
