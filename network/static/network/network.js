
var value_user_id = JSON.parse(document.getElementById("user_id").textContent);
var authentic_id = JSON.parse(document.getElementById("authenticated_id").textContent);

//Main
document.addEventListener('DOMContentLoaded', function(){
    if (authentic_id){
        document.querySelector('#post').style.display = 'block';
        document.querySelector('#follow').addEventListener('click',following_posts);
        document.getElementById('newpost').onsubmit = postPost;
        document.getElementById('image_ch').addEventListener('change', event =>{
            upload_profile_pic(event)})
    }
        
        document.querySelector('#profile').style.display = 'none';
        document.querySelector('#allposts').style.display = 'block';
        document.querySelector('#pages').style.display = 'block';

        loadposts(1);
}
)

function loadposts(x=1){
    if (authentic_id){
    document.getElementById('textarea').innerHTML = "";}
    document.querySelector('#allposts').innerHTML = "";
    document.querySelector('#pages').innerHTML = "";

    // history.pushState({},'', `allposts`);
    fetch(`/allposts?page=${x}`)
    .then(response => response.json())
    .then(posts =>{
        console.log(posts);
        const post = posts.resources;
        post.forEach(add_div);
        
       paginate(posts);
    })
    .catch(error => {
        console.log('Error:', error);
        });
}


function add_div(post,index){
    const element = document.createElement('div');
    element.className='card mx-1 my-2';
    var auth = post.author_id === value_user_id ;
    if (auth){
    var element_a= `
            <div class="card-body" id="id${post.id}">
            <h6 class="card-subtitle mb-2 text-body-secondary">${post.timestamp}</h6>
            <h4 class="card-title" id="idp${index}">
            <img src="${post.author_pic}" height="50px" width="50px">
            <a href="#">${post.author}</a></h4>           
            <p class="card-text">${post.post}</p>
            <button id="liked${post.id}" class="btn btn-primary btn-sm">Like
            <span class="badge text-bg-secondary">${post.likes}</span></button>
            <button type="button" class="btn btn-secondary btn-sm" style="float:right"
            id = "ed${index}">edit Post</button>
            </div>
            `;
    } else {
    var element_a= `
            <div class="card-body" id="id${post.id}">
            <h6 class="card-subtitle mb-2 text-body-secondary">${post.timestamp}</h6>
            <h4 class="card-title" id="idp${index}">
            <img src="${post.author_pic}" height="50px" width="50px">
            <a href="#">${post.author}</a></h4>           
            <p class="card-text">${post.post}</p>
            <button id="liked${post.id}" class="btn btn-primary btn-sm">Like
            <span class="badge text-bg-secondary">${post.likes}</span></button>
            </div>
            `;
    }
    element.innerHTML = element_a;
    document.querySelector('#allposts').append(element);
    document.querySelector(`#idp${index}`).addEventListener('click', ()=> profile(post.author_id));
    if(authentic_id){
    document.querySelector(`#liked${post.id}`).addEventListener('click',()=> like(post.id, index));
    }
    if(auth){document.querySelector(`#ed${index}`).onclick= ()=> editPost(post.id, post.post, post.author_id);}
}


function profile(id) {
    document.querySelector('#post').style.display = 'none';
    document.querySelector('#allposts').style.display = 'block';
    document.querySelector('#profile').style.display = 'block';
    document.querySelector('#pages').style.display = 'block';

    document.querySelector('#pages').innerHTML= '';
    document.querySelector('#allposts').innerHTML= '';

    fetch(`/profiles/${id}`)
    .then(response => response.json())
    .then(person =>{
        console.log(person);
        div_profile(person);
        
            // history.pushState({person:person},'', `profiles/${person[0].user_id}`)
            
        })
        .catch(error => {
            console.log('Error:', error);
        });
    }

    
function div_profile(p){
    document.querySelector('#profile').innerHTML= '';
    const profile_id = p[0].user_id;
    let follow_list = p[0].follower_id
    let following = follow_list.includes(value_user_id);
    const element = document.createElement('div');
    element.className = "container-fluid"
    const elementa= `
    <div class="row p-2" style="justify-content:space-between">
    <div class="row"><img src=${p[0].image} width="100px" height="100px" alt="profile_pic">
    <h1 style="font-size:72px;">${p[0].user}</h1></div>
    <div class="row" style="align-items:center">
        <span class="badge bg-info" style="font-size:28px">Followers: ${p[0].nr_follower}</span>
        <span class="badge bg-info" style="font-size:28px">Following: ${p[0].nr_following}</span>
    </div>
    </div>
    <hr />`;
    const elementb=`
    <div class="row">
        <button type="button" class="btn btn-primary" id="follow_me">Follow</button>
        </div>`;
    const elementc=`
    <div class="row" style="justify-content:space-between">
        <button type="button" class="btn btn-primary" id="follow_me">Unfollow</button>
    </div>`;
    
    
    const posts = p[1].resources;
    posts.forEach(add_div);
    paginate(p[1])
    
    if (profile_id === value_user_id){
        element.innerHTML= elementa;
    }else if (!following){
        element.innerHTML =`<div class="col">${elementa} ${elementb}</div>` ;
    } else {
        element.innerHTML =`<div class="col">${elementa} ${elementc}</div>`;   
    }
    document.querySelector("#profile").append(element);
    if (profile_id !== value_user_id)
    {document.getElementById('follow_me').addEventListener('click',() => follow(profile_id));}
}


function follow(id){
    
    if (document.getElementById('follow_me').innerHTML=== 'Follow')
    {    document.getElementById('follow_me').innerHTML= 'Unfollow';
    }else{
        document.getElementById('follow_me').innerHTML= 'Follow';
    }

    fetch(`/profiles/follow/${id}`)
    .then(response => response.json())
    .then( babo => {
        console.log(babo)
        profile(id);
    }    );
    
}

function following_posts(){
    
    document.querySelector('#post').style.display = 'none';
    document.querySelector('#profile').style.display = 'none';
    document.querySelector('#textarea').innerHTML=""
    document.querySelector('#allposts').innerHTML= '';
    document.querySelector('#pages').innerHTML= '';
    
    fetch('/following')
    .then( response => response.json() )
    .then( data => {
        console.log(data);
        const post = data.resources;
        post.forEach(add_div)
        paginate(data);
    }
    );
}

function paginate(posts){
    document.querySelector('#pages').innerHTML = "";
    const element = document.createElement('div');
    element.className = "pagination justify-content-center" ;
    if (posts.previous !== 0){
        var prev = `
                <span class="page-item"><a href="#" id="page1"> &laquo; first </span></span>
                <span class="page-item"><spa href="#"an id="previous"> previous </span></span>
                `;
        }else{var prev = "";}

    const current = `<span class="page-item">
                    <a href="#"> Page ${posts.current} of ${ posts.total}. </a>
                    </span>`;
              
              
    if (posts.next !== 0){
        var next = `<span class="page-item" > <a href="#" id="next"> next</a> </span>
        <span class="page-item" > <a href="#" id="last">last &raquo;</a> </span>`;
            } else{var next = "";}
            
    const element_paginate = `<span class="step-links" onmouseover="mOver(this)" onmouseout="mOut(this)">
                                ${prev}  ${current}  ${next}
                                </span>`;
    element.innerHTML = element_paginate;
    document.getElementById('pages').append(element);
    
    if(posts.next !== 0){ 
    document.getElementById('next').addEventListener('click',()=> loadposts(posts.next));   
    document.getElementById('last').addEventListener('click', ()=> loadposts(posts.total));
        }
    if(posts.previous !==0){ document.getElementById('previous').addEventListener('click',
                            ()=> loadposts(posts.previous));
                            document.getElementById("page1").addEventListener('click', ()=> loadposts(1)); 
                        }

}

function postPost(){
    var body = document.getElementById('textarea').value;
    const csrftoken = Cookies.get('csrftoken');
    fetch('/posted', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: JSON.stringify({
            body: body
        })
        })        
    .then(response => response.json())
    .then(result => {
        console.log(result);
        document.getElementById('textarea').value = " "
        loadposts(1);
    }).catch(error => {
        console.log('Error:', error);
        });
    return false;
}

function editPost(id, text, author) {
    const element = document.getElementById(`id${id}`);
    element.innerHTML= `
    <form id="editedpost">
        <div class="form-group" style="margin-bottom: 2px";>
        <textarea class="form-control" id="textedit" rows="3">
        ${text}
        </textarea>
        </div>
        <button type="submit" class="btn btn-primary">Post</button>
    </form>
    `;
    document.querySelector('#editedpost').onsubmit = ()=> {
    var post = document.getElementById('textedit').value.trim();
    const csrftoken = Cookies.get('csrftoken');
    fetch(`/edit/${id}`, {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: JSON.stringify({
            post: post
        })
        })        
    .then(response => response.json())
    .then(result => {
        console.log(result);
        profile(author);
    }).catch(error => {
        console.log('Error:', error);
        });
    return false;
    }
}


function like(post_id, index){
  
    var element = document.getElementById(`id${post_id}`);

    fetch(`/liked/${post_id}`)        
    .then(response => response.json())
    .then(post => {
        console.log(post);
        var auth = post.author_id === value_user_id ;
        if (auth){
        element.innerHTML= `
                    <h6 class="card-subtitle mb-2 text-body-secondary">${post.timestamp}</h6>
                    <h4 class="card-title" id="idp${index}">
                    <img src="${post.author_pic}" height="50px" width="50px">
                    <a href="#">${post.author}</a></h4>           
                    <p class="card-text">${post.post}</p>
                    <button id="liked${post.id}" class="btn btn-primary btn-sm">Like
                    <span class="badge text-bg-secondary">${post.likes}</span></button>
                    <button type="button" class="btn btn-secondary btn-sm" style="float:right"
                    id = "ed${index}">edit Post</button>
                    `;
            } else {
        element.innerHTML= `
            <h6 class="card-subtitle mb-2 text-body-secondary">${post.timestamp}</h6>
            <h4 class="card-title" id="idp${index}">
            <img src="${post.author_pic}" height="50px" width="50px">
            <a href="#">${post.author}</a></h4>           
            <p class="card-text">${post.post}</p>
            <button id="liked${post.id}" class="btn btn-primary btn-sm">Like
            <span class="badge text-bg-secondary">${post.likes}</span></button>
            `;}
        document.querySelector(`#liked${post.id}`).addEventListener('click',()=> like(post.id, index));
    });

    return false;
}



const upload_profile_pic = event => {
    event.preventDefault()
    const files = event.target.files
    const formData = new FormData()
    formData.append('image', files[0])

    const csrftoken = Cookies.get('csrftoken');

    fetch(`/image/${value_user_id}`, {
      method: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      mode: 'same-origin',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      document.getElementById('image-up').src = `${data.imageUrl}`;
    })
    .catch(error => {
      console.error(error)
    })
  }




function mOver(obj) {
    obj.style.backgroundColor = "lightgrey";
  }
  
  function mOut(obj) {
    obj.style.backgroundColor = "white"
  }