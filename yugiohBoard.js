
// standard global variables
var container, scene, camera, renderer, controls, stats;
var keyboard = new THREEx.KeyboardState();
var positions = [] 
var cards  = []
var board = {}
var field = [] 
var monsters = {} 
var monster_spawn_states = {"obelisk":[[1.57,0,0],[0,200,0],[200,200,200]],"busterblader":[[0,0,0],[0,0,50],[20,20,20]],"wingeddragon":[[1.57,0,0],[0,250,100],[150,150,150]],"BlueEyes":[[0,0,0],[0,0,50],[5,5,5]]}
for (i=0; i<14; i++) { 
    hz = 600 - 200*(i%7)
    vt = 50 - 650*Math.floor(i/7)  
    positions[i] = [hz,2.5,vt]
    board[i] = [null,null]

}
// custom global variables
var video, videoImage, videoImageContext, videoTexture;

init();
animate();
//Globals 

var cardDimensions = new THREE.CubeGeometry( 150, 5, 480 );
var faceDownArray = [];
faceDownArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
faceDownArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
faceDownArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/back.png' ) }));
faceDownArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
faceDownArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
faceDownArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));

var faceDowncardMaterial = new THREE.MeshFaceMaterial(faceDownArray);

// FUNCTIONS        
function init() 
{
    // SCENE
    scene = new THREE.Scene();
    // CAMERA
    var SCREEN_WIDTH = window.innerWidth, SCREEN_HEIGHT = window.innerHeight;
    var VIEW_ANGLE = 45, ASPECT = SCREEN_WIDTH / SCREEN_HEIGHT, NEAR = 0.1, FAR = 20000;
    camera = new THREE.PerspectiveCamera( VIEW_ANGLE, ASPECT, NEAR, FAR);
    scene.add(camera);

    camera.position.set(0,400,1400);
    camera.lookAt(scene.position);  
    // RENDERER
    if ( Detector.webgl )
        renderer = new THREE.WebGLRenderer( {antialias:true} );
    else
        renderer = new THREE.CanvasRenderer(); 
    renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
    container = document.createElement( 'div' );
    // CSS added so the hidden HTML elements do not reposition this one
    container.style.cssText = "position:absolute;top:0px;left:0px;";
    document.body.appendChild( container );
    container.appendChild( renderer.domElement );
    // CONTROLS
    controls = new THREE.TrackballControls( camera );
    // EVENTS
    THREEx.WindowResize(renderer, camera);
    THREEx.FullScreen.bindKey({ charCode : 'm'.charCodeAt(0) });
    // STATS
    stats = new Stats();
    stats.domElement.style.position = 'absolute';
    stats.domElement.style.bottom = '0px';
    stats.domElement.style.zIndex = 100;
    container.appendChild( stats.domElement );
    // LIGHT
    var light = new THREE.PointLight(0xffffff);
    light.position.set(0,250,0);
    scene.add(light);
    var light2 = new THREE.PointLight(0xffffff);
    light2.position.set(0,250,800);
    scene.add(light2);

    // FLOOR
    var floorTexture = new THREE.ImageUtils.loadTexture( 'custom/yugioh1.jpg' );
    floorTexture.wrapS = floorTexture.wrapT = THREE.RepeatWrapping; 
    floorTexture.repeat.set( 1, 1 );
    var floorMaterial = new THREE.MeshBasicMaterial( { map: floorTexture, side: THREE.DoubleSide } );
    var floorGeometry = new THREE.PlaneGeometry(1500, 2000, 10, 10);
    var floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.position.y = -0.5;
    floor.rotation.x = Math.PI / 2;
    scene.add(floor);
    // SKYBOX/FOG
    // SKYBOX/FOG
    var materialArray = [];
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/dawnmountain-xpos.png' ) }));
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/dawnmountain-xneg.png' ) }));
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/dawnmountain-ypos.png' ) }));
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/dawnmountain-yneg.png' ) }));
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/dawnmountain-zpos.png' ) }));
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/dawnmountain-zneg.png' ) }));


    for (var i = 0; i < 6; i++)
        materialArray[i].side = THREE.BackSide;
    var skyboxMaterial = new THREE.MeshFaceMaterial( materialArray );

    var skyboxGeom = new THREE.CubeGeometry( 5000, 5000, 5000, 1, 1, 1 );

    var skybox = new THREE.Mesh( skyboxGeom, skyboxMaterial );
    scene.add( skybox );    

    // a little bit of scenery...
    var ambientlight = new THREE.AmbientLight(0x111111);
    scene.add( ambientlight );
    ///////////
    // VIDEO //
    ///////////

    video = document.getElementById( 'monitor' );

    videoImage = document.getElementById( 'videoImage' );
    videoImageContext = videoImage.getContext( '2d' );
    // background color if no video present
    videoImageContext.fillStyle = '#000000';
    videoImageContext.fillRect( 0, 0, videoImage.width, videoImage.height);

    videoTexture = new THREE.Texture( videoImage );
    videoTexture.minFilter = THREE.LinearFilter;
    videoTexture.magFilter = THREE.LinearFilter;

    var movieMaterial = new THREE.MeshBasicMaterial( { map: videoTexture, overdraw: true, side:THREE.DoubleSide } );
    // the geometry on which the movie will be displayed;
    //      movie image will be scaled to fit these dimensions.
    var movieGeometry = new THREE.PlaneGeometry( 760, 650, 1, 1 );
    var movieScreen = new THREE.Mesh( movieGeometry, movieMaterial );
    movieScreen.position.set(0,300,-1000);
    scene.add(movieScreen);

    // pseudo-border for plane, to make it easier to see
    var planeGeometry = new THREE.CubeGeometry( 810, 675, 1, 1 );
    var planeMaterial = new THREE.MeshBasicMaterial( { color: 0x000000 } );
    var movieback = new THREE.Mesh( planeGeometry, planeMaterial );
    movieback.position.set(0,300,-1010);
    scene.add(movieback);

    //camera.position.set(0,150,300);
    //camera.lookAt(movieScreen.position);
    /*
     var loader = new THREE.ColladaLoader();
     loader.options.convertUpAxis = true;
     loader.load('collada-models/girl.DAE', function (result) {
     scene.add(result.scene);
 });
*/
    // torus knot
    //(150,height,480)
    //card height 
    var cubeGeometry = new THREE.CubeGeometry( 150, 5, 480 );
    materialArray = [];
    //cards with 
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/back.png' ) }));
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
    materialArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
    //  new THREE.MeshBasicMaterial({ color: 0x000088 });

        //y should be 1/2 of height

    //center back head is 0,3.5,-600. 
    //the midpoint is always 250 z units back. 

    //Deck
    //cards with 
    var deckArray = [];

    deckArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern_deck.jpg' ) }));
    deckArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern_deck.jpg' ) }));
    deckArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/back.png' ) }));
    deckArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern_deck.jpg' ) }));
    deckArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern_deck.jpg' ) }));
    deckArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern_deck.jpg' ) }));
    //  new THREE.MeshBasicMaterial({ color: 0x000088 });
    var deckMaterial = new THREE.MeshFaceMaterial(deckArray);
    var deckGeometry = new THREE.CubeGeometry( 150, 50, 480 );

    deck = new THREE.Mesh( deckGeometry, deckMaterial ); 

    deck.position.set(-600,25,-600);
    scene.add(deck);

}

function animate() 
{
    requestAnimationFrame( animate );
    render();       
    update();
}

function update()
{       
    if ( keyboard.pressed("p") ) // pause
        video.pause();
    if ( keyboard.pressed("r") ) // resume
        video.play();
    controls.update();
    stats.update();
}

function test () {
    card = new THREE.Mesh( cardDimensions, faceDownCardMaterial );
    card.position.set(400,2.5,-600);scene.add(card);
    card = new THREE.Mesh( cardDimensions, cardMaterial );


}
function render() 
{   
videoImageContext.drawImage( video, 0, 0, videoImage.width, videoImage.height );
if ( videoTexture ) {
    videoTexture.needsUpdate = true;
}

renderer.render( scene, camera );
}

function play_card(position,name,state) { 
    rendered = false
    if (board[position][1] == "att" ) {
        rendered = true  
    }
    board[position] = [name,state]


    if (state == "down"){ 
        var cubeMaterial = new THREE.MeshFaceMaterial(faceDownArray);
        var card = new THREE.Mesh( cardDimensions, faceDowncardMaterial );
        card.position.set(positions[position][0],positions[position][1],positions[position][2])
        cards[position] = card
    
        scene.add(card) 

    }

    else {

var cardUpDimensions = new THREE.CubeGeometry( 150, 320, 5);
var faceUpArray = [];
faceUpArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
faceUpArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
faceUpArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
faceUpArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/pattern.jpg' ) }));
faceUpArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/back.png' ) }));
faceUpArray.push(new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'images/back.png' ) }));

var faceUpcardMaterial = new THREE.MeshFaceMaterial(faceUpArray);


        faceUpArray[4] = new THREE.MeshBasicMaterial( { map: THREE.ImageUtils.loadTexture( 'custom/'+name+".png") });
        var cubeMaterial = new THREE.MeshFaceMaterial(faceUpArray);
        var card = new THREE.Mesh( cardUpDimensions, faceUpcardMaterial);
        card.position.set(positions[position][0],positions[position][1]+160,positions[position][2]+5)
        cards[position] = card
        scene.add(card) 
        if (!rendered) {
            render_monster(position) 
        }
              
    }


}
function render_monster(position) { 
    var loader = new THREE.OBJMTLLoader()
    var name = board[position][0]
    loader.addEventListener( 'load', function ( event ) {
					var object = event.content;
					object.position.set(positions[position][0],positions[position][1],positions[position][2]);
					scene.add( object );
                    monsters[name] = object
                    rotation = monster_spawn_states[name][0]
                    position = monster_spawn_states[name][1]
                    scale = monster_spawn_states[name][2]
                    object.scale.set(scale[0],scale[1],scale[2]) 

                    axis = ['x','y','z']
                    for (i=0;i<3;i++){
                        object.rotation[axis[i]] = rotation[i] 
                        object.position[axis[i]] += position[i]
                    }
	});
    loader.load( 'monsters/'+ name + '.obj', 'monsters/' + name + '.mtl' );


}
var ws = new WebSocket("ws://pythonscript.denerosarmy.com:8000/ws");
ws.onopen = function() {
    ws.send("Hello, world");
};
ws.onmessage = function (evt) {
    if (evt.data == "ATTACK"){ 
        attack() 
    }
    obj = JSON.parse(evt.data)
    console.log("message received")
    console.log(JSON.stringify(obj))
    for (i=0;i<14;i++){ 
        if (board[i][0] == null || (obj[i] != null && obj[i] != board[i][1]))
        {
            if (obj[i] != null) {
                play_card(i,obj[i]["name"],obj[i]["state"]) 
            }
        }
    }

};

function attack() {
	window.location = "http://localhost:8000/kaiba.html";
}

