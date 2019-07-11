
window.onscroll = () => {
  const filter = document.getElementById("schedule-filter-container");
  const trigger = filter.offsetTop / 1.2;
  if(window.pageYOffset > trigger){ //After Scrolling
    filter.classList.remove("schedule-filter__dont-stick");
    document.getElementById("schedule-filter-toggle").disabled = false;
  } else { //When scroll back to top
    filter.classList.add("schedule-filter__dont-stick");
    document.getElementById("schedule-filter-toggle").disabled = true;
  }
};

const updateFilter = function (e) {
    const justChecked = e.checked;
    const name = e.name;
    const value = e.value;
    let thisFilterBlock = document.getElementsByName(name);


    if (value == 'all' && justChecked == false) {
        e.checked = true;
        return;
    }

    if (value == 'all' && justChecked == true) {
        for (let i = 0; i < thisFilterBlock.length; i++) {
            if (thisFilterBlock[i].value !== 'all') {
                thisFilterBlock[i].checked = false;
            }
        }
    }

    if (value !== 'all' && justChecked == true) {
        for (let i = 0; i < thisFilterBlock.length; i++) {
            if (thisFilterBlock[i].value == 'all') {
                thisFilterBlock[i].checked = false;
                break;
            }
        }
    }

    if (value !== 'all' && justChecked == false) {
        let atLeastOneTrue = false;
        for (let i = 0; i < thisFilterBlock.length; i++) {
            if (thisFilterBlock[i].checked == true) {
                atLeastOneTrue = true;
                break;
            }
        }
        if (atLeastOneTrue == false) {
            for (let i = 0; i < thisFilterBlock.length; i++) {
                if (thisFilterBlock[i].value == 'all') {
                    thisFilterBlock[i].checked = true;
                    updateStateBlock(thisFilterBlock, true);
                    return;
                }
            }
        }
    }

    if (value !== 'all') {
        updateStateBlock(thisFilterBlock);
    } else {
        updateStateBlock(thisFilterBlock, true);
    }
}

const updateStateBlock = function (filterBlock, all) {
    const name = filterBlock[0].name;
    //console.log('Updating the state for ' + name +'!');
    //console.log(filterBlock);
    if (all === undefined) {
        for (let i = 0; i < filterBlock.length; i++) {
            if (filterBlock[i].value == 'all') continue;
            STATE[name][filterBlock[i].value] = filterBlock[i].checked;
        }
    }
    if (all === true) {
        for (let i = 0; i < filterBlock.length; i++) {
            if (filterBlock[i].value == 'all') continue;
            STATE[name][filterBlock[i].value] = true;
        }
    }

    filter(STATE);
}


const filter = function (state) {
    clearAllFilters(state);

    const categories = Object.keys(state);
    for (let i = 0; i < categories.length; i++) {
        let categoryName = categories[i];
        let categoryData = state[categories[i]];
        let modifierProperty = categoryData.modifier[0];
        let modifierValue = categoryData.modifier[1];

        let targetsToHide = removeFromArray(Object.keys(categoryData), 'modifier').filter(function (ele) {
            return !categoryData[ele];
        });

        for (let j = 0; j < targetsToHide.length; j++) {
            //console.log('Searching for: [data-'+categoryName+'="'+targetsToHide[j]+'"]');
            //console.log('Adding ' + modifierProperty +':'+modifierValue);
            let modifiedElements = document.querySelectorAll('[data-' + categoryName + '="' + targetsToHide[j] + '"]');
            for (let k = 0; k < modifiedElements.length; k++) {
                modifiedElements[k].style[modifierProperty] = modifierValue;
            }
        }
    }
};

const clearAllFilters = function (state) {
    const categories = Object.keys(state);
    for (let i = 0; i < categories.length; i++) {
        let categoryName = categories[i];
        let categoryData = state[categories[i]];
        let modifierProperty = categoryData.modifier[0];

        let targets = removeFromArray(Object.keys(categoryData), 'modifier');

        for (let j = 0; j < targets.length; j++) {
            let cleanElements = document.querySelectorAll('[data-' + categoryName + '="' + targets[j] + '"]');
            for (let k = 0; k < cleanElements.length; k++) {
                cleanElements[k].style[modifierProperty] = null;
            }
        }
    }
}


const removeFromArray = (arr, value) => {
    return arr.filter((ele) => {
        return ele != value;
    });
}

const filterToggle = document.getElementById('schedule-filter-toggle');

filterToggle.addEventListener('click', function () {
    const filterContainer = document.getElementById('schedule-filter-container');

    filterContainer.classList.toggle('schedule-filter__container--show');
});
