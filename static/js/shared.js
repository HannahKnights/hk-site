// functions...

var colours = [
    'burlywood',
    'cabetblue',
    'chartreuse',
    'indianred',
    'darkorange',
    'moccasin',
    'yellow',
    'mediumspringgreen',
    'lightskyblue',
    'cornflowerblue',
    'sandybrown'
]

function roll_the_dice(min_num, max_num) {
    /*
        generates a random number for a range.

        arguments:
            - min number
            - max number
    */
    return (Math.floor(Math.random() * (max_num - min_num + 1)) + min_num);
};

function clear_spinning_images() {
    // remove currently spinning images
    $('.front').addClass('hidden').removeClass('front');
    $('.back').addClass('hidden').removeClass('back');
}

function set_spinning_images() {
    // set new spinning images
    if ($('[data-attr="' + window.spin_count + '"]').hasClass('text')) {
        $('[data-attr="' + window.spin_count + '"]').css('background-color', colours[roll_the_dice(0, colours.length-1)])
    };
    $('[data-attr="' + window.spin_count + '"]').addClass('front').removeClass('hidden');
    if ($('[data-attr="' + (window.spin_count + 1) + '"]').hasClass('text')) {
        $('[data-attr="' + (window.spin_count + 1) + '"]').css('background-color', colours[roll_the_dice(0, colours.length-1)])
    };
    $('[data-attr="' + (window.spin_count + 1) + '"]').addClass('back').removeClass('hidden');
}

function you_spin_me_round() {
    // spin the images round
    window.spin_count = window.spin_count > window.image_count - 1 ? 1 : window.spin_count;
    clear_spinning_images();
    set_spinning_images();
    window.spin_count += 2;
}

function create_shuffled_list(low_number, high_number) {
    // create a randomly ordered lists of numbers
    var shuffle_list = [];
    for (var i = low_number; i <= high_number; i++) {
        shuffle_list.push(i);
    }
    shuffle_list.sort(function() { return 0.5 - Math.random() });
    return shuffle_list;
}

function fake_load_image(image_num, image_list) {
    // fake it until you make it
    var image_source = image_list.get(image_num).src;
    $('<img/>').attr('src', image_source).on('load', function() {
       $(this).remove();
       window.image_load_count += 1;
       // once 80% of the images are loaded we are ready to go
       window.ready_to_go = (window.image_load_count >= (window.image_count*0.8)) ? true : false;
    });
}

function fake_load_all_images() {
    //sort all the images by the data attr
    var sorted_images = images.sort(function(this_img, next_image) {
        var this_img_sort = $(this_img).attr('data-attr');
        var next_img_sort = $(next_image).attr('data-attr');

        return this_img_sort - next_img_sort;
    })
    // loop through them and load all
    for (image_num in sorted_images) {
        fake_load_image(image_num, sorted_images);
    }
};

function add_random_order_to_images() {
    // randomly order the list of images
    var image_num = '';
    var image_list = create_shuffled_list(1, window.image_count);
    console.log(image_list)
    // loop through images and add data-attr
    for (var i = 1; i <= window.image_count; i++) {
        image_num = image_list[i - 1].toString();
        $(window.images.get(i - 1)).attr('data-attr', image_num);
    }
    fake_load_all_images();
}

function dot_dot_dot() {
    // ...
    $('.beginning').html($('.beginning').html().replace('&nbsp;','&nbsp;.'));
}

function clear_intro() {
    // spinning is beginning..
    $('.beginning').hide();
}

function start_spinning() {
    clear_intro();
    you_spin_me_round();
    setInterval(function() {you_spin_me_round()}, 5000);
}

function check_loaded_images_and_start_spinning(begin_page_event) {
    dot_dot_dot();
    if (window.seconds_count >= 5 && window.ready_to_go) {
        clearInterval(begin_page_event);
        start_spinning();
    } else if (window.seconds_count >= 30) {
        // it has been 30 seconds lets start spinner anyway...
        clearInterval(begin_page_event);
        start_spinning();
    }
    window.seconds_count += 1;
}

function here_we_begin() {
    console.log('here we begin...')
    add_random_order_to_images();
    var begin_page_event = setInterval(function(){
        check_loaded_images_and_start_spinning(begin_page_event);
    }, 1000)

}

$(document).ready( function() {
    // set spinning stuff values
    window.images = $("img").add($("div.text"));
    window.image_count = window.images.length;
    window.image_load_count = 0;
    window.spin_count = 1;
    window.ready_to_go = false;
    window.seconds_count = 0;

    // spin stuff...
    here_we_begin();
})
