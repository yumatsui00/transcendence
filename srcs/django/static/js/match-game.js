
document.addEventListener('DOMContentLoaded', (event) => {
    const roomName = window.roomName;  // グローバル変数から値を取得
    const url = `wss://${window.location.host}/ws/game/${roomName}/`;
    console.log(`WebSocket URL: ${url}`);

    const socket = new WebSocket(url);

    const canvas = document.getElementById('gameCanvas');
    const renderer = new THREE.WebGLRenderer({ canvas });
    renderer.setSize(window.innerWidth, window.innerHeight);

    const scene = new THREE.Scene();

    //カメラ
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.x = 0;
    camera.position.y = 0;
    camera.position.z = 4;
    camera.rotation.x = Math.PI / 6;

    const boadGeometry = new THREE.BoxGeometry(5, 8, 0);
    const boadMaterial = new THREE.MeshBasicMaterial({ color: 0x0095DD });
    const boad = new THREE.Mesh(boadGeometry, boadMaterial);
    boad.position.x = 0;
    boad.position.y = 4;
    boad.position.z = 0;
    scene.add(boad);

    const sideGeometry = new THREE.BoxGeometry(0.1, 8, 0.2);
    const sideMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });
    const side1 = new THREE.Mesh(sideGeometry, sideMaterial);
    side1.position.x = 2.55;
    side1.position.y = 4;
    side1.position.z = 0;
    scene.add(side1);
    const side2 = new THREE.Mesh(sideGeometry, sideMaterial);
    side2.position.x = -2.55;
    side2.position.y = 4;
    side2.position.z = 0;
    scene.add(side2);

    const dotGeometry = new THREE.BoxGeometry(0.2,0.1,0.01);
    const dotMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });
    for (let i = 0; i < 17; i++) {
        const dot = new THREE.Mesh(dotGeometry,dotMaterial);
        dot.position.x = -2.4 + i*0.3;
        dot.position.y = 4;
        dot.position.z = 0;
        scene.add(dot);
    }
    
    const radiusTop = 0.2; // 上面の半径
    const radiusBottom = 0.2; // 底面の半径
    const height = 0.2; // 高さ
    const radialSegments = 32; // 円周の分割数

    const cylinderGeometry = new THREE.CylinderGeometry(radiusTop, radiusBottom, height, radialSegments);
    const cylinderMaterial = new THREE.MeshStandardMaterial({ color: 0xDD3300  });
    const cylinder = new THREE.Mesh(cylinderGeometry, cylinderMaterial);
    cylinder.rotation.x = Math.PI / 2;
    cylinder.position.y = 4;
    scene.add(cylinder)

    const cylinderEdgeGeometory = new THREE.EdgesGeometry(cylinderGeometry);
    const cylinderEdgesMaterial = new THREE.LineBasicMaterial({ color: 0x8B0000});
    const cylinderEdge = new THREE.LineSegments(cylinderEdgeGeometory,cylinderEdgesMaterial);
    cylinderEdge.position.copy(cylinder.position);
    cylinderEdge.rotation.copy(cylinder.rotation);
    scene.add(cylinderEdge);

    const barGeometry = new THREE.BoxGeometry(1.2, 0.1, 0.2);
    const barMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });
    const bar1 = new THREE.Mesh(barGeometry, barMaterial);
    bar1.position.y = 0.2;
    scene.add(bar1);
    const barEdgeGeometory = new THREE.EdgesGeometry(barGeometry);
    const barEdgesMaterial = new THREE.LineBasicMaterial({ color: 0x000000});
    const barEdge1 = new THREE.LineSegments(barEdgeGeometory,barEdgesMaterial);
    barEdge1.position.copy(bar1.position);
    barEdge1.rotation.copy(bar1.rotation);
    scene.add(barEdge1);

    const bar2 = new THREE.Mesh(barGeometry, barMaterial);
    bar2.position.y = 7.8;
    scene.add(bar2);
    const barEdge2 = new THREE.LineSegments(barEdgeGeometory,barEdgesMaterial);
    barEdge2.position.copy(bar2.position);
    barEdge2.rotation.copy(bar2.rotation);
    scene.add(barEdge2);

    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate();

    //socetの設定はここから
    socket.onopen = function(e) {
        console.log('WebSocket connection established');
    };
    
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const ballPosition = data.ball_position;
        // ボールの座標を更新する処理
    };
    
    socket.onclose = function(e) {
        console.log('WebSocket connection closed');
    };
});


    // let ballDirection = { x: 0.02, y: 0.02 };

//     function animate() {
//         requestAnimationFrame(animate);
//         renderer.render(scene, camera);

//         ball.position.x += ballDirection.x;
//         ball.position.y += ballDirection.y;

//         if (ball.position.y > 2.5 || ball.position.y < -2.5) {
//             ballDirection.y = -ballDirection.y;
//         }

//         if (ball.position.x > 4.5 || ball.position.x < -4.5) {
//             ballDirection.x = -ballDirection.x;
//         }

//         socket.send(JSON.stringify({
//             action: 'update_ball_position',
//             x: ball.position.x,
//             y: ball.position.y
//         }));
//     }

//     socket.onopen = function() {
//         console.log('WebSocket connection opened');
//         animate();
//     };

//     socket.onmessage = function(e) {
//         const data = JSON.parse(e.data);
//         if (data.action === 'ball_position_update') {
//             ball.position.x = data.x;
//             ball.position.y = data.y;
//         } else if (data.action === 'score_update') {
//             console.log(`Score - Player 1: ${data.player1}, Player 2: ${data.player2}`);
//         } else if (data.action === 'game_over') {
//             alert(`Game Over! Winner: ${data.winner}`);
//             socket.close();
//         }
//     };
// });