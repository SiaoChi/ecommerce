var updateBtns = document.getElementsByClassName('update-cart')
// var deleteBtns = document.getElementsByClassName('delete-cart')


for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
			addCookieItem(productId, action)
	})
}

function addCookieItem(productId, action){
	console.log('使用者無登入');

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1};

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'spcode'){
		if (cart[spCode] == undefined){
		cart[spCode] = {'spCode':oninput()}
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted');
			delete cart[productId];
		}
	}

	if (action == 'delete'){
		console.log('delete item');
		delete cart[productId];

	}


	console.log('CART:', cart);
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";

}

$( ".update-page" ).on('click',function() {
	location.reload()

  	// $( ".item-num" ).load('/cart/ .item-num');
  	// $("#item-total").load('/cart/ #item-total');
  	// $( "#order-num" ).load('/cart/ #order-num');
  	// $("#order-total").load('/cart/ #order-total');

});

$( ".update-shop" ).on('click',function() {
  	$( ".shop-footer" ).load('/ .shop-footer');
});





// 更新shop購物車數量
// function updateShop(){
// 	let url = 'update_cookie/'
//
// 	fetch(url, {
// 			method:'GET',
// 			headers:{
// 				'Content-Type':'application/json',
// 				// 'X-CSRFToken':csrftoken,
// 			},
// 			// body:JSON.stringify({'delivery': text })
// 		})
// 		.then((response) => {
// 		   return response.json();
//
// 		})
// 		.then((data) => {
// 			let json = JSON.parse(data)
// 			console.log(typeof json)
// 			let result = document.getElementById('update-shop');
// 			result.innerHTML='';
// 			result.innerHTML='('+ json.get_cart_items +')'
// 			console.log('!js work')
// 		})
//
// }




function updateDeliver() {
	var select = document.getElementById('id_delivery')
	var index = select.selectedIndex
	var text = select.options[index].text

	let url = 'update_deliver/'


	fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,

			},
			body:JSON.stringify({'delivery': text })
		})
		.then((response) => {

		   return response.json()

			// console.log('1111',response)

		})
		.then((data) => {
			console.log(typeof data)
			let json = JSON.parse(data)
			console.log(typeof json)
			let result = document.getElementById('show-deliver');
			result.innerHTML='';
			result.innerHTML='<h6>運送方式:'+ json.delivery +'</h6>'
			//  document.querySelector('#delivery_fee').innerHTML(request.session['delivery'])
			console.log('js work')
		})

}

function onSubmit(token) {
     document.getElementById("demo-form").submit();
   }






