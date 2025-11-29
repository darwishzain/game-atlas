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
        albiononline_resource(data,content);
        //for(const key in data['tools']){
        //    content.innerHTML += image("","",data.tools[key]['img']);
//
        //}
        //for(const key in data['resources']){
        //    content.innerHTML += image("","",data.resources[key]['img']);
        //}
    });
}

function albiononline_resource(data,content)
{
    content.innerHTML += `<h3>I don't know how to represent the data that makes it understandable. And I can't connect to hotspot for internet when I'm live, so I can't see the images</h3>`;
    for(const key in data.resources)
    {
        content.innerHTML += `<h5 style='text-align:center;'>${key}(<a href=''>${data.resources[key].name})<img src='${data.resources[key]['img']}' alt=''></a></h5>`;
    }
}
function image(text,url,image){
    html = "<a href=''><img src='"+image+"' alt=''></a>";
    return html;
}