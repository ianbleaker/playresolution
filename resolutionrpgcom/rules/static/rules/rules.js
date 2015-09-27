/**
 * Created by ian on 9/24/2015.
 */
$( document).ready(function(){
	$(".button-collapse").sideNav({
        edge: 'right'
    });
    $('#rules-nav').localScroll({
		//target: '#content', // could be a selector or a jQuery object too.
        offset: -130,
		duration:200,
		hash:false,
		onBefore:function( e, anchor, $target ){
			// The 'this' is the settings object, can be modified
		},
		onAfter:function( anchor, settings ){
			// The 'this' contains the scrolled element (#content)
		}
	});
});