function main(){
    var width = window.innerWidth;
    var height = window.innerHeight;
    var aspect = width / height;

    var scene = new THREE.Scene();
    scene.background = new THREE.Color( 0x050490 );

    info = document.querySelector("#info");
    popup = document.querySelector("#popup");

    var camera = new THREE.PerspectiveCamera( 60, aspect, 1, 1000 );

    var renderer = new THREE.WebGLRenderer({antialias: true});
    renderer.setSize( width, height );
    document.body.appendChild( renderer.domElement );

    var light = new THREE.DirectionalLight( 0xffffff, 2 );
    light.position.set( 5, 2, 5 );
    light.lookAt( 0, 0, 0 );
    // var lh = new THREE.DirectionalLightHelper(light);
    // scene.add(lh);
    scene.add( light );

    var size = 50;
    var divisions = 100;

    var gridHelper = new THREE.GridHelper( size, divisions );
    gridHelper.position.y = -1.5;
    scene.add( gridHelper );

    $.ajax({
        url: "http://localhost:8000/api/get_rooms/",
        success: function (resp) {
            resp = JSON.parse(resp);

            for (var i = 0; i < resp.length; ++i) {
                var room = [resp[i]["location_x"], resp[i]["location_z"], resp[i]["location_y"]];

                var geometry = new THREE.BoxGeometry( .8, .8, .8 );

                // mesh
                var material = new THREE.MeshStandardMaterial( {
                        color: 0x050490,
                        polygonOffset: true,
                        polygonOffsetFactor: 1, // positive value pushes polygon further away
                        polygonOffsetUnits: 1
                } );
                var mesh = new THREE.Mesh( geometry, material );

                // wireframe
                var geo = new THREE.EdgesGeometry( mesh.geometry ); // or WireframeGeometry
                var mat = new THREE.LineBasicMaterial( { color: 0xffffff, linewidth: 2 } );
                var wireframe = new THREE.LineSegments( geo, mat );
                mesh.add( wireframe );

                var cube = new THREE.Mesh( geometry, material );
                
                cube.position.set(...room);
                mesh.position.set(...room);
                mesh.userData.room = resp[i];
                cube.userData.room = resp[i];

                scene.add( cube );
                scene.add( mesh );
            }
        }
    });
    
    camera.position.set( 10, 2, 10 );
    camera.lookAt(0,0,0);

    const directions = {
        'w': new Vector3( 0, 0,-1),
        's': new Vector3( 0, 0, 1),
        'a': new Vector3(-1, 0, 0),
        'd': new Vector3( 1, 0, 0),
        'q': new Vector3( 0, 1, 0),
        'e': new Vector3( 0,-1, 0),
    }

    const handleKeyBoardInput = (evt) => {
        if (directions[evt.key]) {
            let delta = directions[evt.key].clone();
            delta.applyEuler(look);
            delta.multiplyScalar(0.1);
            camera.position.add(delta);
        }
    }

    window.onkeypress = handleKeyBoardInput;

    var canvas = renderer.domElement;
    // var pointerLocked = false;
    var look = camera.rotation.clone().reorder( "YXZ" );

    var is_drag_state = false;

    canvas.onmousedown = function( evt ) {
        is_drag_state = true;
    };

    canvas.onmousemove = function( evt ) {
        if (is_drag_state) {
            const x = - evt.movementY / 500;
            const y = - evt.movementX / 500;
            look.x -= x;
            look.y -= y;
            camera.rotation.copy( look );
        }
    };

    canvas.onmouseup = function( evt ) {
        is_drag_state = false;
    };

    prv_active = undefined;
    curr_active = undefined;

    document.addEventListener("mousemove", (e) => {
        // normalized device coordinates
        var mouse = {};
        mouse.x = ( e.clientX / window.innerWidth ) * 2 - 1;
        mouse.y = - ( e.clientY / window.innerHeight ) * 2 + 1;

        if (flag == 0) {
            var raycaster = new THREE.Raycaster();

            raycaster.setFromCamera( mouse, camera );

            var intersects = raycaster.intersectObjects( scene.children );
            if (intersects.length == 0) {
                curr_active = undefined;
            } else {
                curr_active = intersects[ 0 ].object;
            }

            if (prv_active && prv_active.type == "Mesh") {
                prv_active.material.color = new THREE.Color( 0x050490 );
            }
            
            if (curr_active && curr_active.type == "Mesh") {
                curr_active.material.color = new THREE.Color( 0xff0000 );
            }
            prv_active = curr_active;

            if(curr_active && curr_active.type == "Mesh"){
                info.style.visibility = "visible";
                var x = curr_active.position.x;
                var y = curr_active.position.y;
                var z = curr_active.position.z;
                info.textContent = `Room Number: ${curr_active.userData.room['room_no']}\nRoom Location: ${x},${y},${z}\n`;
            }
            else {
                info.style.visibility = "hidden";
                info.textContent = ``;
            }
        }
    });
    
    flag = 0;
    locked_room = undefined;

    canvas.onclick = function () {
        if (curr_active != undefined && curr_active.type == "Mesh") {
            popup.style.visibility = "visible";
            // lock 
            flag ^= 1;
            console.log(flag);
            if (flag) {
                locked_room = curr_active;
            } else {
                locked_room = undefined;
                hide_box();
            }
        }
    };

	function animate() {
		requestAnimationFrame( animate );
		renderer.render( scene, camera );
	}

	animate();
}

window.onload = main;

function hide_box() {
    popup.style.visibility = "hidden";
}

function add_preference() {
    $.ajax({
        url: "http://localhost:8000/api/add_preference/1/",
        method: "POST",
        success: function(resp) {
            console.log(resp);
        },
        error: function(a, b, c) {
            console.log(c);
        }
    });
}

function remove_preference() {

}
