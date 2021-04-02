const updateBtns = document.querySelectorAll('.update-cart')

function clickCartBtn() {
    var productId = this.dataset.product;
    var action = this.dataset.action;

    if(user == 'AnonymousUser') {
        addCookieItem(productId, action);
    } else {
        updateUserOrder(productId, action);
    }
}

function addCookieItem(productId, action) {
    if (action == 'add') {
        if(!cart[productId]) {
            cart[productId] = {'quantity': 1};
        } else {
            cart[productId]['quantity'] += 1;
        }
    } else if (action == 'remove') {
        cart[productId]['quantity'] -= 1;
        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    }
    updateCartCookie(cart);
    location.reload();
}

function updateUserOrder(productId, action) {
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        location.reload();
    })
}

updateBtns.forEach(button => button.addEventListener('click', clickCartBtn))