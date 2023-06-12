const url = window.location.href.split("/")
const categoryID = url[url.length-1].split("-")[0]
const categoryName = url[url.length-1].split("-")[1]

const sort_btn = document.querySelector('.sort-btn');
const sort_options = document.querySelector('.sort-options');

var isOpen = false;

sort_btn.addEventListener('click', () => {
    if(isOpen){
        sort_options.classList.remove('sort-options-active');
        isOpen = false;
    }
    else{
        sort_options.classList.add('sort-options-active');
        isOpen = true;
    }
})


const sort_value = document.querySelector('.sort-val');

const price_hfirst = document.querySelector('#price-highest-first');

price_hfirst.addEventListener('click', () => {
    document.location.href = '/./category-sorted/'+categoryID+'-'+categoryName+'-PriceHighestFirst';
    sort_value.innerHTML = "Price (Highest First)";
    sort_options.classList.remove('sort-options-active');
    isOpen = false;
})


const price_lfirst = document.querySelector('#price-lowest-first');

price_lfirst.addEventListener('click', () => {
    document.location.href = '/./category-sorted/'+categoryID+'-'+categoryName+'-PriceLowestFirst';
    sort_value.innerHTML = "Price (Lowest First)";
    sort_options.classList.remove('sort-options-active');
    isOpen = false;
})


const popularity = document.querySelector('#popularity');

popularity.addEventListener('click', () => {
    document.location.href = '/./category-sorted/'+categoryID+'-'+categoryName+'-LatestFirst';
    sort_value.innerHTML = "Latest";
    sort_options.classList.remove('sort-options-active');
    isOpen = false;

})

