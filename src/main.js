const params = new URLSearchParams(window.location.search);
const game = params.get('game');
const content = document.getElementById('content');
if (game) {
    document.getElementById('title').innerText = `Game Atlas@${game}`;
    if(game === 'albiononline'){albiononline();}
}

function albiononline(){
    fetch('../data/mmorpg/albiononline.json')
    .then(response => response.json())
    .then(data => {
        document.title = `gameatlas@${data['title']}`;
        content.innerHTML += `<h1>${data['title']}</h1>`;
        for(const key in data['tools']){
            content.innerHTML += image("","",data.tools[key]['img']);

        }
        for(const key in data['resources']){
            content.innerHTML += image("","",data.resources[key]['img']);
        }
    });
}

function image(text,url,image){
    html = "<a href=''><img src='"+image+"' alt=''></a>";
    return html;
}