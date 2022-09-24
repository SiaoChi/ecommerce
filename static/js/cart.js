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

// // 按了加入購物車或是調整物品數量時的功能
// function addCookieItem(productId, action){
// 	console.log('User is authenticated, sending data...')
//
// 		var url = 'update_item/'
//
// 		fetch(url, {
// 			method:'POST',
// 			headers:{
// 				'Content-Type':'application/json',
// 			},
// 			body:JSON.stringify({'productId':productId, 'action':action})
// 		})
// 		.then((response) => {
// 		   return response.json();
// 		})
// 		.then((data) => {
// 		    location.reload()
// 		});
// }


// function updateUserOrder(productId, action){
// 	console.log('User is authenticated, sending data...')
//
// 		var url = '/update_item/'
//
// 		fetch(url, {
// 			method:'POST',
// 			headers:{
// 				'Content-Type':'application/json',
// 				'X-CSRFToken':csrftoken,
// 			},
// 			body:JSON.stringify({'productId':productId, 'action':action})
// 		})
// 		.then((response) => {
// 		   return response.json();
// 		})
// 		.then((data) => {
// 		    location.reload()
// 		});
// }
//
function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
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


	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

	location.reload()
}

