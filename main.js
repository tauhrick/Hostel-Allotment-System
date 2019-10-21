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
    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x050490);
    var camera = new THREE.PerspectiveCamera(60, width/height, 1, 1000);

    var renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );

    for (var i = 0; i < rooms.length; ++i) {
        var geometry = new THREE.BoxGeometry( .8, .8, .8 );

				// mesh
				var material = new THREE.MeshBasicMaterial( {
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

    var controls = new THREE.OrbitControls( camera, renderer.domElement );

    camera.position.set(-2, 5, -5);
    //camera.lookAt(5,0,5);
    controls.update();

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
            delta.multiplyScalar(0.1);
            camera.position.add(delta);
        }
    }

    window.onkeypress = handleKeyBoardInput;	

	function animate() {
		requestAnimationFrame( animate );
        controls.update();
		renderer.render( scene, camera );
	}
	animate();
}

window.onload = main;
