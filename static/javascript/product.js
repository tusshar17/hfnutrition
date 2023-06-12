let pics = document.getElementsByClassName('pic-change-btn')

let focusedImg = document.getElementsByClassName('focused-img')

for(var i=0; i<pics.length; i++){
    pics[i].addEventListener('mouseover', function(){

        if(focusedImg.length>0){
            focusedImg[0].classList.remove('focused-img')
        }

        this.classList.add('focused-img')
        document.getElementById('product-main-pic').src = this.src
    })
}