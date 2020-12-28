document.addEventListener("DOMContentLoaded", function(){

    var spacing_x = 60;
    var spacing_y = 120;
    // Initialize Flowy
    flowy(document.getElementById("canvas"), onGrab, onRelease, onSnap, onRearrange, spacing_x, spacing_y);

    function onGrab(block){
        // When a user grabs a block
        
    };
    function onRelease(){
        // When a user lets go of a block w/ no parent

    };
    function onSnap(block, first, parent){
        // When a block snaps with another one. True allows snapping.
        if (!block.classList.contains("task") && block.querySelector("#task-id")) {
            block.querySelector("#multiCollapseExample2").style.display = "none";
            for (let index = 0; index < block.children[0].children.length; index++) {
                if (block.children[0].children[index].id == "task-id") {
                    block.children[0].children[index].style.display = "none";
                }
            }
        }
        return true;
    };
    function onRearrange(block, parent){
        // When a block is rearranged. True forces released block to snap back to original parent
        
    };

    var reset_graphing_canvas = document.getElementById("resetGraphingCanvas");
    reset_graphing_canvas.addEventListener("click", function(){
        var planner_head = document.getElementById('plannerHead');
        // Clears graphing canvas
        flowy.deleteBlocks();
        planner_head.innerHTML = 'Goal Planner ' + '<i class="fas fa-sitemap"></i>';
    });

    var open_load_modal = document.getElementById("loadOpen");
    open_load_modal.addEventListener("click", function() {
        // Opens load plan modal and loads in list of user's plans
        var selectBox = document.getElementById('selectFile');
        var length = selectBox.options.length;
        // Clear select options
        for (i = length-1; i >= 0; i--) {
            selectBox.options[i] = null;
        }
        // Loading Animation
        var elements_to_show_hide = [
            document.getElementById('planLabelCol'),
            document.getElementById('planListCol')
        ]
        var loading_img = document.getElementById('planListLoading');
        let plan_list_loading_animation = new Loading_Animation(loading_img, elements_to_show_hide);
        plan_list_loading_animation.start_animation();
        // Get list of user's plans from server
        $.getJSON('/list_plans', {}, function(data) {
            if (data.plan_list) {
                // Load list of user's plans as select options
                for(var i = 0, l = data.plan_list.length; i < l; i++){
                    var option = data.plan_list[i];
                    // End Loading Animation
                    plan_list_loading_animation.stop_animation();
                    selectBox.options.add( new Option(option.text, option.value) );               
                }
            }
        })
    });

    var delete_btn = document.getElementById("deletePlan");

    delete_btn.addEventListener("click", function() {
        var selectBox = document.getElementById('selectFile');
        var planToDeleteText = selectBox.options[selectBox.selectedIndex].text;
        var planToDeleteVal = selectBox.options[selectBox.selectedIndex].value;

        document.getElementById("deleteval").value = planToDeleteVal;
        document.getElementById("planToDelete").innerHTML = "Delete Plan: "  + planToDeleteText + "?"
    });

    function confirm_delete() {
        document.getElementById("deleteForm").submit();
    }

    
    var save_plan = document.getElementById('save');
    save_plan.addEventListener("click", function() {
        // Saves user plan currently drawn on canvas
        var test = JSON.stringify(flowy.output());
        var plan_name = $('#plan_name').val();
        var plan_description = $('#plan_description').val();
        // Send plan name and data to server
        $.ajax({
        url: '/save_graph',
        data: JSON.stringify({
            'plan_name': plan_name,
            'plan_description': plan_description,
            'plan_graph': JSON.stringify(flowy.output())
        }),
        contentType: 'application/json',
        type: 'POST',
        success: function(response) {
            // Show response messages
            $("#saveResponseMessage").text(response.message);
            $("#saveResponseModal").modal('show');
            // Show overwrite prompt
            if (response.saved == 0) {
                $("#overwriteSave").show();
            } else {
                // Otherwise only save confirmation message
                $("#overwriteSave").hide();
            }
        },
        error: function(error) {
            console.log(error);
        }
        }).done(function(response) {
            if (response.saved == 1) {
                $('#plannerHead').html(plan_name + ' ' + '<i class="fas fa-sitemap"></i>');
            }
        });
    });

    var overwrite_plan = document.getElementById('overwriteSave');
    overwrite_plan.addEventListener('click', function() {
        // Overwrites existing user plan         
        var plan_name = $('#plan_name').val();           
        var plan_description = $('#plan_description').val();                                                           
        // Send plan name and data to server
        $.ajax({
            url: '/overwrite_graph',
            data: JSON.stringify({
                'plan_name': plan_name,
                'plan_description': plan_description,
                'plan_graph': JSON.stringify(flowy.output())    
            }),
            contentType: 'application/json',
            type: 'POST',
            success: function(response) {
                // Hide overwrite elements
                $('#overwriteSave').hide();
                // Show save confirmation message
                $("#saveResponseMessage").text(response.message);
                $("#saveResponseModal").modal('show');
            },
            error: function(error) {
                console.log(error);
            }
        }).done(function() {
            $('#plannerHead').html(plan_name + ' ' + '<i class="fas fa-sitemap"></i>');
        });
    });

    var load_plan = document.getElementById('loadPlan');
    load_plan.addEventListener('click', function() {
        // Loads plan into canvas
        // Get plan data from server
        $.getJSON('/load_graph', {
            plan_to_load: $('#selectFile').children("option:selected").val()
        }, function(data) {
                
                var canvas_element = document.getElementById("canvas");
                // Load plan chart into canvas
                //canvas_element.innerHTML = data.plan_data['html'];
                // Load chart data into flowy object
                flowy.import(data.plan_data);
            }).done(function(data) {
                $('#plannerHead').html(data.plan_name + ' ' + '<i class="fas fa-sitemap"></i>');
            });
    });


    function Loading_Animation(loading_img, elements_to_show_hide) {
        this.elements = [];
        this.loading_img = loading_img;
        for (var i = 0; i < elements_to_show_hide.length; i++) {
            this.elements.push(elements_to_show_hide[i]);
        }
    }

    Loading_Animation.prototype.start_animation = function() {
        for (var element of this.elements) {
            element.style.display = "none";
        }
        this.loading_img.style.display = "";
    }

    Loading_Animation.prototype.stop_animation = function() {
        for (var element of this.elements) {
            element.style.display = "";
        }
        this.loading_img.style.display = "none";
    }
    
});

    