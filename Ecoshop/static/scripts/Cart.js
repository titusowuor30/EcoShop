 console.log('hello')
var updatebtns=document.getElementsByClassName('update-cart')

for(var i=0;i<updatebtns.length;i++){
   updatebtns[i].addEventListener('click',function(){
   var productId=this.dataset.product
   var action=this.dataset.action
   console.log('productId:',productId,'action:',action)

    console.log('USER:',user)

    if(user=='AnonymousUser'){
    console.log('user not logged in')
    }else{
      updateUserOrder(productId,action)
    }
   })
}


function updateUserOrder(productId,action){
console.log('user is authenticated ,sending data..')

var url='/cart/update-item/'

fetch(url, {
      method:'POST',
      headers:{
      'Content-Type':'Application/json',
      'X-CSRFToken':csrftoken,
      },
      body:JSON.stringify({'productId:':productId,'action:':action})
      })
       .then((response) =>{
        return response.json()
        })
      .then((data) =>{
     console.log('data',data)
      })
}