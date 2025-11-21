document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('starCanvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        class Star {
            constructor() {
                this.reset();
            }

            reset() {
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.size = Math.random() * 2;
                this.speed = Math.random() * 0.5 + 0.2;
            }

            update() {
                this.y -= this.speed;
                if (this.y < 0) {
                    this.x = Math.random() * width;
                    this.y = height;
                    this.size = Math.random() * 2;
                    this.speed = Math.random() * 0.5 + 0.2;
                }
            }

            draw() {
                ctx.fillStyle = "white";
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        const stars = [];
        const starCount = 250; // Reduzido para melhor performance

        for (let i = 0; i < starCount; i++) {
            stars.push(new Star());
        }

        function animate() {
            ctx.clearRect(0, 0, width, height);

            for (let star of stars) {
                star.update();
                star.draw();
            }

            requestAnimationFrame(animate);
        }

        animate();

        /* Ajusta o canvas ao redimensionar a tela */
        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });
    }
});
