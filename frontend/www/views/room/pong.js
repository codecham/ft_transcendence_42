import * as THREE from 'three'
import {UnrealBloomPass} from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import {EffectComposer} from 'three/examples/jsm/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/examples/jsm/postprocessing/RenderPass.js';
import {FontLoader} from 'three/examples/jsm/loaders/FontLoader.js'; 
import {TextGeometry} from 'three/examples/jsm/geometries/TextGeometry.js';
import {OutputPass} from 'three/examples/jsm/postprocessing/OutputPass.js';
import {ShaderPass} from 'three/examples/jsm/postprocessing/ShaderPass.js';

  
let group;
var camera, scene, renderer;
var renderScene, bloomComposer, bloomPass, mixPass, bloomLayer, finalComposer, outputPass;
var BLOOM_SCENE = 1;
var darkMaterial, materials; 
var Globe, Globe2;
var P1, P2;
var ballMesh;
var stars, starsGroup;
var scoreLeft = 0;
var scoreRight = 0;
var textMesh;
var font = undefined;
let isRendering = false;
let renderContainer = document.getElementById("pongDiv") 
let firstGame = true;

const params = {
	threshold: 0,
	strength: 0.25,
	radius: 0.5,
	exposure: 1
};

var p1_y;
var p2_y;
var ball_x;
var ball_y;
var p1_score = 0;
var p2_score = 0;
var status;
var winner;
var loser;



  /////
  
	  /* INITIALISATION DU JEU MODEL 3D, TEXTURE, ETC, ... */
  
  /////
  
export function  init() {
	bloomLayer = new THREE.Layers();
	bloomLayer.set( BLOOM_SCENE );
	darkMaterial = new THREE.MeshBasicMaterial( { color: 'black' } );
	  materials = {};
  
	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setPixelRatio( window.devicePixelRatio * 1);
	renderer.setSize(window.innerWidth, window.innerHeight);
	renderer.toneMapping = THREE.ReinhardToneMapping;
	renderContainer.appendChild( renderer.domElement ); // modification pour mettre le jeu dans une div
  
  
	scene = new THREE.Scene();
	camera = new THREE.PerspectiveCamera( 45, window.innerWidth/window.innerHeight);
	camera.position.z = 5;
	camera.position.x = 0;
	camera.position.y = -15;
	camera.position.z = 10;
	camera.lookAt(scene.position);
  
	renderScene = new RenderPass( scene, camera );
  
	bloomPass = new UnrealBloomPass( new THREE.Vector2( window.innerWidth, window.innerHeight ), 1.5, 0.4, 0.85 );
	bloomPass.threshold = params.threshold;
	bloomPass.strength = params.strength;
	bloomPass.radius = params.radius;
  
	bloomComposer = new EffectComposer( renderer );
	bloomComposer.renderToScreen = false;
	bloomComposer.addPass( renderScene );
	bloomComposer.addPass( bloomPass );
	mixPass = new ShaderPass(
	  new THREE.ShaderMaterial( {
		uniforms: {
		  baseTexture: { value: null },
		  bloomTexture: { value: bloomComposer.renderTarget2.texture }
		},
		vertexShader: document.getElementById( 'vertexshader' ).textContent,
		fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
		defines: {}
	  } ), 'baseTexture'
	);
	mixPass.needsSwap = true;
  
	outputPass = new OutputPass();
  
	finalComposer = new EffectComposer( renderer );
	finalComposer.addPass( renderScene );
	finalComposer.addPass( mixPass );
	finalComposer.addPass( outputPass );
  
	group = new THREE.Group();
	scene.add(group);
	loadFont();
}
  
  
  //init side wall in 3D
export function  wall3d() {
	scene.traverse(disposeMaterial);
	scene.children.length = 0;
	//init Wall number one
	const gem = new THREE.BoxGeometry(12,0.2,0.2);
	const material2  = new THREE.MeshBasicMaterial({color: 0xffffff });
	const box2  = new THREE.Mesh(gem , material2 );
	scene.add(box2);
	box2.position.x = 0;
	box2.position.y = 4;
	box2.position.z = 0.25;
	box2.castShadow = true;
  
	//init Wall number two
	const gem2 = new THREE.BoxGeometry(12,0.2,0.2);
	const material3  = new THREE.MeshBasicMaterial({color: 0xffffff});
	const box3  = new THREE.Mesh(gem2 , material3 );
	scene.add(box3);
	box3.position.x = 0
	box3.position.y = -4
	box3.position.z = 0.25
	box3.castShadow = true
	box2.layers.toggle(BLOOM_SCENE);
	box3.layers.toggle(BLOOM_SCENE);
}
  
  //init player in 3d
  
export function  player3d() {
	// scene.traverse( disposeMaterial );
	// scene.children.length = 0;
	const player1 = new THREE.BoxGeometry(0.2,1.5,0.2);
	const materialP1  = new THREE.MeshBasicMaterial({color: 0xb81818});
	P1  = new THREE.Mesh(player1 , materialP1 );
	scene.add(P1);
	P1.position.x = 6;
	P1.position.y = 0;
	P1.position.z = 0.25;
	P1.castShadow = true;
	
	const player2 = new THREE.BoxGeometry(0.2,1.5,0.2);
	const materialP2  = new THREE.MeshBasicMaterial({color: 0x1b18b8});
	P2  = new THREE.Mesh(player2 , materialP2 );
	scene.add(P2);
	P2.position.x = -6;
	P2.position.y = 0;
	P2.position.z = 0.25;
	P2.castShadow = true;
	P1.layers.toggle(BLOOM_SCENE);
	P2.layers.toggle(BLOOM_SCENE);
}
  
  
export function  ball3d() {
	// scene.traverse( disposeMaterial );
	// scene.children.length = 0;
	const ball = new THREE.BoxGeometry(0.2,0.2,0.2);
	const materialBall  = new THREE.MeshBasicMaterial({color: 0xffffff});
	ballMesh  = new THREE.Mesh(ball , materialBall);
	scene.add(ballMesh);
	ballMesh.position.z = 0.2;
	ballMesh.position.x = 0;
	ballMesh.position.y = 0;
	ballMesh.layers.toggle(BLOOM_SCENE);
}
  
export function  line3d() {
	// scene.traverse( disposeMaterial );
	// scene.children.length = 0;
	const line1 = new THREE.PlaneGeometry( 0.1, 0.8 );
	const materialLine1 = new THREE.MeshBasicMaterial( {color: 0xffffff, side: THREE.DoubleSide} );
	const plane1 = new THREE.Mesh( line1, materialLine1 );
	scene.add( plane1 );
	plane1.position.y = 3.5;
	
	const line2 = new THREE.PlaneGeometry( 0.1, 0.8 );
	const materialLine2 = new THREE.MeshBasicMaterial( {color: 0xffffff, side: THREE.DoubleSide} );
	const plane2 = new THREE.Mesh( line2, materialLine2 );
	scene.add( plane2 );
	plane2.position.y = 2;
	
	const line3 = new THREE.PlaneGeometry( 0.1, 0.8 );
	const materialLine3 = new THREE.MeshBasicMaterial( {color: 0xffffff, side: THREE.DoubleSide} );
	const plane3 = new THREE.Mesh( line3, materialLine3 );
	scene.add( plane3 );
	plane3.position.y = 0.5;
	
	const line4 = new THREE.PlaneGeometry( 0.1, 0.8 );
	const materialLine4 = new THREE.MeshBasicMaterial( {color: 0xffffff, side: THREE.DoubleSide} );
	const plane4 = new THREE.Mesh( line4, materialLine4 );
	scene.add( plane4 );
	plane4.position.y = -1;
	
	const line5 = new THREE.PlaneGeometry( 0.1, 0.8 );
	const materialLine5 = new THREE.MeshBasicMaterial( {color: 0xffffff, side: THREE.DoubleSide} );
	const plane5 = new THREE.Mesh( line5, materialLine5 );
	scene.add( plane5 );
	plane5.position.y = -2.5;
	plane1.layers.toggle(BLOOM_SCENE);
	plane2.layers.toggle(BLOOM_SCENE);
	plane3.layers.toggle(BLOOM_SCENE);
	plane4.layers.toggle(BLOOM_SCENE);
	plane5.layers.toggle(BLOOM_SCENE);
}
  
  
  
export function  initStars() {
	starsGroup = new THREE.Group();
	scene.add(starsGroup);
	const starsGeometry = new THREE.BufferGeometry();
	const starsMaterial = new THREE.PointsMaterial({ color: 0xFFFFFF, size: 1 });
  
	const starsVertices = [];
  
	for (let i = 0; i < 1000; i++) {
		const x = (Math.random() - 0.5) * 2000;
		const y = (Math.random() - 0.5) * 2000;
		const z = (Math.random() - 0.5) * 2000;
  
		starsVertices.push(x, y, z);
	}
  
	starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
	stars = new THREE.Points(starsGeometry, starsMaterial);
  
	starsGroup.add(stars);
	starsGroup.layers.toggle(BLOOM_SCENE);
}
  
  
  
export function  globe() {
	var Globe_g = new THREE.IcosahedronGeometry(2, 4); 
	var Points_g = new THREE.BufferGeometry();
	Points_g.vertices = Globe_g.vertices;
  
	Globe = new THREE.Mesh( Globe_g, new THREE.MeshBasicMaterial({ wireframe: !0,  color: 'red'}) );
	Globe2 = new THREE.Mesh( Globe_g, new THREE.MeshBasicMaterial({ wireframe: !0, color: 'blue' }) );
  
	var Points = new THREE.Points(Points_g, new THREE.PointsMaterial({ size: 0.75 }) );
  
	Globe.add(Points);
	Globe2.add(Points);
	scene.add(Globe);
	scene.add(Globe2);
	Globe.position.x = 15;
	Globe.position.y = 15;
	Globe2.position.x = -15;
	Globe2.position.y = 15;
	Globe.layers.toggle(BLOOM_SCENE);
	Globe2.layers.toggle(BLOOM_SCENE);
}
  
function loadFont() {
  
	const loader = new FontLoader();
	loader.load( '../../assets/font/arcade.json', function ( droidFont ) {
  
	  font = droidFont;
  
	  refreshText();
	} );
  
}
  
function initText() {
  
	const textGeometry = new TextGeometry(scoreLeft + ' : ' + scoreRight, {
		  size: 1,
		  height: 0.2,
		  curveSegments: 10,
		  font: font,
	  });
	  textGeometry.center();
	  textGeometry.translate(0, 5 , 0);
	  textGeometry.rotateX(90)
	  const textMaterial = new THREE.MeshBasicMaterial({color: 0xffffff});
	  textMesh = new THREE.Mesh(textGeometry, textMaterial);
	  textMesh.layers.toggle(BLOOM_SCENE);
		// scene.add(textMesh);
	  group.add(textMesh);
}

function refreshText() {
  
	group.remove(textMesh);
	initText();
}
  
  /////
  
	  /* BLOOM EFFECT */
  
  /////
  
function disposeMaterial( obj ) {
	
	if ( obj.material ) {
		obj.material.dispose();
	}
}
	
function darkenNonBloomed( obj ) {
	
	if ( obj.isMesh && bloomLayer.test( obj.layers ) === false ) {
		materials[ obj.uuid ] = obj.material;
		obj.material = darkMaterial;
	}
}
	
function restoreMaterial( obj ){
	
	if ( materials[ obj.uuid ] ) {
		obj.material = materials[ obj.uuid ];
		delete materials[ obj.uuid ];
	}
}
  

  
/*window.onresize = function (){
  
	  const width = window.innerWidth;
	  const height = window.innerHeight;
	
	  camera.aspect = width / height;
	  camera.updateProjectionMatrix();
	
	  renderer.setSize( width, height );
	
	  bloomComposer.setSize( width, height );
	  finalComposer.setSize( width, height );
	
	  render();
	
};*/
	
  
export function  startGame() {
	isRendering = true;
	renderContainer.style.display = 'block';
	if (firstGame == true) {
		init();
		wall3d();
		player3d();
		line3d();
		ball3d();
		initStars();
		globe();
		firstGame = false;
	}
	render();
}

export function stopGame() {
	isRendering = false;
	renderContainer.style.display = 'none';
}

export function recievedata(data) {
	p1_y = data.p1_posY;
	p2_y = data.p2_posY;
	ball_x = data.ball_posX;
	ball_y = data.ball_posY;
	p1_score = data.p1_score;
	p2_score = data.p2_score;
}

function	updatedata()
{
	P2.position.y = p1_y
	P1.position.y = p2_y
	ballMesh.position.x = ball_x
	ballMesh.position.y = ball_y
	scoreLeft = p1_score;
	scoreRight = p2_score;
}

function render () {
	if (isRendering) {
		requestAnimationFrame(render);
		scene.traverse( darkenNonBloomed );
		bloomComposer.render();
		scene.traverse( restoreMaterial );
		starsGroup.rotation.x += 0.0002;
		starsGroup.rotation.y += 0.0002;
		Globe.rotation.x += 0.001;
		Globe.rotation.y += 0.001;
		Globe2.rotation.x += 0.001;
		Globe2.rotation.y += 0.001;
		updatedata();
		loadFont();
		scene.add(group);
		finalComposer.render();	
	}	
	
};
