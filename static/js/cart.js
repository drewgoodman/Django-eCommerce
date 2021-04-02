const updateBtns = document.querySelectorAll('.update-cart')

function clickCartBtn() {
    var productId = this.dataset.product;
    var action = this.dataset.action;

    if(user == 'AnonymousUser') {
        console.info('user is not authenticated')
    } else {
        updateUserOrder(productId, action);
    }
}

function updateUserOrder(productId, action) {
    console.info('user is authenticated, send data')
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
        console.log('Data: ', data)
        location.reload();
    })
}

updateBtns.forEach(button => button.addEventListener('click', clickCartBtn))