var rooms = [
    [4, 1, 0],
    [5, 1, 0],
    [6, 1, 0],
    [7, 1, 0],
    [8, 1, 0],
    [1, 4, 0],
    [1, 5, 0],
    [1, 6, 0],
    [1, 7, 0],
    [1, 8, 0],
    [4, 3, 0],
    [5, 3, 0],
    [6, 3, 0],
    [7, 3, 0],
    [8, 3, 0],
    [3, 4, 0],
    [3, 5, 0],
    [3, 6, 0],
    [3, 7, 0],
    [3, 8, 0],  

    [4, 1, 1],
    [5, 1, 1],
    [6, 1, 1],
    [7, 1, 1],
    [8, 1, 1],
    [1, 4, 1],
    [1, 5, 1],
    [1, 6, 1],
    [1, 7, 1],
    [1, 8, 1],
    [4, 3, 1],
    [5, 3, 1],
    [6, 3, 1],
    [7, 3, 1],
    [8, 3, 1],
    [3, 4, 1],
    [3, 5, 1],
    [3, 6, 1],
    [3, 7, 1],
    [3, 8, 1],

    [4, 1, -1],
    [5, 1, -1],
    [6, 1, -1],
    [7, 1, -1],
    [8, 1, -1],
    [1, 4, -1],
    [1, 5, -1],
    [1, 6, -1],
    [1, 7, -1],
    [1, 8, -1],
    [4, 3, -1],
    [5, 3, -1],
    [6, 3, -1],
    [7, 3, -1],
    [8, 3, -1],
    [3, 4, -1],
    [3, 5, -1],
    [3, 6, -1],
    [3, 7, -1],
    [3, 8, -1],
];

function main(){
    var width = window.innerWidth;
    var height = window.innerHeight;
    var aspect = width / height;

    var scene = new THREE.Scene();
    scene.background = new THREE.Color( 0x050490 );

    var camera = new THREE.PerspectiveCamera( 60, aspect, 1, 1000 );

    var renderer = new THREE.WebGLRenderer();
    renderer.setSize( width, height );
    document.body.appendChild( renderer.domElement );

    var light = new THREE.DirectionalLight( 0xffffff, 2 );
    light.position.set( 5, 2, 5 );
    light.lookAt( 0, 0, 0 );
    var lh = new THREE.DirectionalLightHelper(light);
    scene.add(lh);
    scene.add( light );

    var size = 50;
    var divisions = 100;

    var gridHelper = new THREE.GridHelper( size, divisions );
    gridHelper.position.y = -1.5;
    scene.add( gridHelper );

    for (var i = 0; i < rooms.length; ++i) {
        var geometry = new THREE.BoxGeometry( .8, .8, .8 );

        // mesh
        var material = new THREE.MeshStandardMaterial( {
                color: 0x050490,
                polygonOffset: true,
                polygonOffsetFactor: 1, // positive value pushes polygon further away
                polygonOffsetUnits: 1
        } );
        var mesh = new THREE.Mesh( geometry, material );
        scene.add( mesh )

        // wireframe
        var geo = new THREE.EdgesGeometry( mesh.geometry ); // or WireframeGeometry
        var mat = new THREE.LineBasicMaterial( { color: 0xffffff, linewidth: 2 } );
        var wireframe = new THREE.LineSegments( geo, mat );
        mesh.add( wireframe );

        var cube = new THREE.Mesh( geometry, material );
        cube.position.set(rooms[i][0], rooms[i][2], rooms[i][1]);
        mesh.position.set(rooms[i][0], rooms[i][2], rooms[i][1]);
        scene.add( cube );
    }

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
    var pointerLocked = false;
    var look = camera.rotation.clone().reorder( "YXZ" );

    canvas.onclick = function () {
        this.requestPointerLock();
    }

    document.addEventListener('pointerlockchange', () => {
        if (document.pointerLockElement === canvas) {
            pointerLocked = true;
        } else {
            pointerLocked = false;
        }
        console.log("pointer locked:", pointerLocked);
    });

    var prv_active;
    var curr_active;

    document.addEventListener("mousemove", (e) => {
        if (!pointerLocked) {
            // normalized device coordinates
            var mouse = {};
            mouse.x = ( e.clientX / window.innerWidth ) * 2 - 1;
            mouse.y = - ( e.clientY / window.innerHeight ) * 2 + 1;

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
        } else {
            const x = - e.movementY / 500; //  +ve, up  / -ve, down  //
            const y = - e.movementX / 500; // +ve, left / -ve, right //
            look.x += x;
            look.y += y;
            camera.rotation.copy(look);
        }
    });

	function animate() {
		requestAnimationFrame( animate );
		renderer.render( scene, camera );
	}

	animate();
}

window.onload = main;
