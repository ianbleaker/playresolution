/**
 * Created by ian on 9/24/2015.
 */
$('#rules-nav').localScroll({
		target: 'body', // could be a selector or a jQuery object too.
		duration: 150,
		offset: -135,
		hash:false
});
$('.section-content-ex').addClass('well');
$('.section-title-ex').html('<i class="mdi-action-subject"></i>').addClass('shadow-z-1');