$( document).ready(function(){

    //create left menu sidenav, close when click some a link
	$("#left-menu-button").sideNav({
        edge: 'left',
        closeOnClick: true
    });

    //move the hidden mobile nav menu, then unhide it (but it will be below nav bar)
    $(function (){
        relativeTopLoop(-60, -60, ".mobile-nav-li");
        $("#mobile-nav-buttons").removeClass("hidden");
    });

    //when you click the mobile nav button (right menu button), toggle the mobile menu
     var rmb = $("#right-menu-button");
    $(rmb).on('click', function() {
        if ($(rmb).hasClass("open")){
            $(rmb).removeClass("open");
            relativeTopLoop(-60, -60, ".mobile-nav-li");
            makeOpaque(0, ".mobile-nav-li");
        }
        else {
            $(rmb).addClass("open");
            relativeTopLoop(0, 10, ".mobile-nav-li");
            makeOpaque(1, ".mobile-nav-li");
        }
    });

    //when the mobile nav is open, if you click anywhere except the menu, it closes the menu
    $('body').click(function(event) {
        if($(rmb).hasClass("open")) {
            if (!($(event.target).closest($(rmb)).length || $(event.target).closest($("#mobile-nav-ul")).length)) {
                $(rmb).removeClass("open");
                relativeTopLoop(-60, -60, ".mobile-nav-li");
                makeOpaque(0, ".mobile-nav-li");
            }
        }
    });
});

function sectionsLoaded(){
    //move the generated skill table inside the skill list div
    $("#skill-list-table").detach().appendTo($("#skill-list-title").next());

    //wrap tables in divs
    $(".section-content").each(function(){
        //wrap multi tables all together
        $(this).find(".multi-table").wrapAll("<div class='multi-table-div'></div>");
        //wrap single tables that aren't multi tables in own div
        $(this).find(".table").not(".multi-table").wrap("<div class='table-div'></div>");
    });
}

function bookmarksLoaded(){
    //create a scrollspy that makes the links active and opens/closes on scroll
    function sectionScrollSpy() {
        $(".scrollspy").each(function () {
            var position = $(this).position();
            var max = position.top
                + $(this).height()
                + parseInt(($(this).css("padding-bottom")).replace("px", ""))
                + parseInt(($(this).css("margin-bottom")).replace("px", ""))
                + parseInt(($(this).css("border-bottom-width")).replace("px", ""))
                + parseInt(($(this).css("padding-top")).replace("px", ""))
                + parseInt(($(this).css("margin-top")).replace("px", ""))
                + parseInt(($(this).css("border-top-width")).replace("px", ""));
            //do scrollspy
            $(this).scrollspy({
                //set positions - use all borders, margin and padding to get accurate results
                min: position.top,
                max: max,
                //on enter, add classes
                onEnter: function (element, position) {
                    //get all uls for the link id
                    var ul = $("#" + $(element).attr("id") + "-ul");
                    //add active class to a with same id
                    $("#" + $(element).attr("id") + "-a").addClass("active");
                    //add active class to link with same id
                    if ($(ul).css("display") == "none") {
                        $(ul).slideDown();
                        $(ul).prev(".left-menu-reveal").addClass("open").removeClass("closed");
                    }
                },
                onLeave: function (element, position) {
                    //get ul for link id
                    var ul = $("#" + $(element).attr("id") + "-ul");
                    //remove active class
                    $("#" + $(element).attr("id") + "-a").removeClass("active");
                    if ($(ul).css("display") == "block") {
                        $(ul).slideUp();
                        $(ul).prev(".left-menu-reveal").addClass("closed").removeClass("open");
                    }
                }
            });
        });
    }

    sectionScrollSpy();
    $( window).resize(function(){sectionScrollSpy();});

    //start all ul-wrappers in the slide up position
    $(".left-menu-ul-wrapper").slideUp();

    $('.bookmarks-menu').localScroll({
        offset: -64,
        duration: 300,
        hash: false
    });

    //make arrows on bookmark menu reveal ULs underneath through sliding
	$(".left-menu-reveal").click(function (){
        if($(this).hasClass("closed")){
            $(this).removeClass("closed");
            $(this).addClass("open");
            $(this).next("div").slideDown();
        }
        else if ($(this).hasClass("open")){
            $(this).removeClass("open");
            $(this).addClass("closed");
            $(this).next("div").slideUp();
        }
    });
}

function setActiveLink(linkTitle){
	$("."+linkTitle+"-a").addClass("active");
}

function relativeTopLoop(start, per, elements){
    $(elements).each(function () {
        $(this).css("top", start + "px");
        start += per;
    });
}

function makeOpaque(opacityValue, elements){
    $(elements).css("opacity", opacityValue);
}

//slugify functionality
function slugify(text){
    return text.toLowerCase().replace(/-/g,' ').replace(/[^\w ]+/g,'').replace(/ +/g,'-');
}