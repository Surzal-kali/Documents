# (❁´◡`❁) Next Steps

## The Machines

### 1.)  Earth=207 (Apache, Ubuntu 16.04)

        It needs some deal with crypotgraphy (my only weakness) and the secure messaging service. I need to decipher the three past messages listed in the site, to gain access to the admin panel for the website and bust permissions.

        #### The Messages:
        The messages are encrypted with the "name" of the sender, which is interesting, as well as reversing the string before encrypting it. I don't know the actual encryption method, so fuck this level. Yet its the oldest one of the lot, it deserves retirment. I'm sick of seeing that shitty stock image on my network.

        The Message encryption is XOR with base 32 on top. Below are the deobfuscated messages
        VMFMNUKBDZMI…YWE
        VPZWEKGQ7QYK…PV
        VPZWEKGQ7QYK…KJ7

        Which translated from BASE36 is
        Riddle 1: 4162295637467353600
        Riddle 2: 4175322795757723000
        Riddle 3: 4175322795757723000


        ## The Admin Panel:
        So the admin panel is a little funky fresh feeling. upon logging in with the correct username, but incorrect password, it gives me a CSRF verification failed. This is the most plaintext way to say "hack here" i have ever seen in my life.



                                        HTTP/1.1 403 Forbidden
                        Date: Mon, 04 May 2026 11:01:39 GMT
                        Server: Apache/2.4.51 (Fedora) OpenSSL/1.1.1l mod_wsgi/4.7.1 Python/3.9
                        Content-Length: 1019
                        X-Frame-Options: DENY
                        X-Content-Type-Options: nosniff
                        Referrer-Policy: same-origin
                        Keep-Alive: timeout=5, max=100
                        Connection: Keep-Alive
                        Content-Type: text/html; charset=UTF-8


                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta http-equiv="content-type" content="text/html; charset=utf-8">
                        <meta name="robots" content="NONE,NOARCHIVE">
                        <title>403 Forbidden</title>
                        <style type="text/css">
                        html * { padding:0; margin:0; }
                        body * { padding:10px 20px; }
                        body * * { padding:0; }
                        body { font:small sans-serif; background:#eee; color:#000; }
                        body>div { border-bottom:1px solid #ddd; }
                        h1 { font-weight:normal; margin-bottom:.4em; }
                        h1 span { font-size:60%; color:#666; font-weight:normal; }
                        #info { background:#f6f6f6; }
                        #info ul { margin: 0.5em 4em; }
                        #info p, #summary p { padding-top:10px; }
                        #summary { background: #ffc; }
                        #explanation { background:#eee; border-bottom: 0px none; }
                        </style>
                        </head>
                        <body>
                        <div id="summary">
                        <h1>Forbidden <span>(403)</span></h1>
                        <p>CSRF verification failed. Request aborted.</p>


                        </div>

                        <div id="explanation">
                        <p><small>More information is available with DEBUG=True.</small></p>
                        </div>

                        </body>
                        </html>


### 2.)  Marlinspike=55 (Apache, Ubuntu 16.04)

        My favorite one right now OHMYGOD. Its a fishtank. Its amazing. Its got a guest account that operates in the system memory. And its HELLA OUTDATED BABY. So we're going to work on this one concurrently with earth, as it will serve as a pivot point for the next machines. It even resets the box on power off. so lets never turn this thing off unless we absolutely fucked up. Yeth.

        #### The Guest Bin:

        It seriously has so many different ways it can be hacked, because the container is leaked, so it spills into the system files (barely, its a misconfiguration and a bug after all). 
        So we can read the guest profile default bin, the way it's cron jobs are, and how it backups its files despite being ephemeral. The virtual "virtual" network is known as Windows Network, so both the container and the vm are concurrently running, and the End Goal is on a seperate virtualx2 network. This inception bullshit makes my head hurt.

        ### Update Logs:

    --- So Marlin is a fishtank. Its amazing. Its got a guest account that operates in the system memory. And its HELLA 
	outdated. It even resets the box on power off. so lets never turn this thing off unless we absolutely fucked 
	something up k. cool. The guest account is extremely interesting to its level of being able to traverse the system 
	files. There must be a symbolic link or authoratative issue going on here. The wordpress installation is key, because 
	if we can upload and traverse its source code directly through the guest account, surely we will find the break like 
	we did Porteus. The fact that it is a wordpress installation is also interesting, as it is likely that there are 
	vulnerabilities in the wordpress installation that can be exploited. 

	---Backup Storage
	Everything lives in tmp for the login screen, but i still think i can use this somehow.
	Its missing a child-process, duplicity. How convenient for me. 
	I can use this to my advantage, as it is likely that there is something hidden in the backup storage. 
	The fact that it is missing means it can be supplied. And we have a text-editor.
	According to the Extended Partition, we have 4.3 GB of swap size in the guest login.


    --- The Guest Bin:
	It has mysql. The site dynamically loads all of its content off an api call.
	This could be my injection point for the actual root account.
	In addition, the vm sits on Proxmox, but also has a container with ubuntu desktop. 
	with an outdated version of ubuntu 16.04. So there are likely vulnerabilities 
	Theres something in the underlying system that can be exploited.

	Vmwarectrl, which is interesting considerin
	I don't know what part of the system the guest account is. 
	It could honestly be trapped inside of a leaky container. Its barely 
	doing anything in Proxmox's eyes. So we first have to pivot 
	through a database, outside of a VM, just to get root. I 
	like it. Also, old printer drivers if i recall correctly 
	have vulnerabilities with their data. So 
	hp-config_usb_printer could be an entry point as well. The 
	right malware and we're in.

	The virtual "virtual" network is known as Windows Network, so both the container and the vm are concurrently running. 
	This inception bullshit makes my head hurt.

	### The Injection Point
	www.10.0.0.55/secret/wp-admin/Index.php. 
	It can be rewritten from guest. But theres no need
	http://10.0.0.55/secret/wp-admin/ is the login page we inject :D

	So bad news, the injection point doesn't exist, simply for the simple fact the site is so fucked up that it doesn't even load. So we have to find another path to the next foothold. Web payload ahoy!

	### Alternative Methods
	We have the ability to connect to a remote server from the guest client. So if we 
	serve a web payload HERE. We don't have to use the shitty text editor installed, and 
	instead make something amazing :D. 
	After looking deeper into the system configuration, or as far as you can from an 
	insecure guest account, it seems the guest account, along with saving to tmp, can 
	back tmp and read the /var/ folders in there entirety. This is interesting, as it 
	means we can read the mysql configuration files, and likely get the credentials for the mysql database. 

	Next steps include crafting a malicious payload to make the guest account give us the tmp account password, and maybe more!


### 3.) Porteus=157 (Python3 HTTP Web Server)

        --- Porteus is a dual web server boot to root machine. It has a python3 http web server, and a countdown timer that is vulnerable to cross-site scripting. So we will be working on this one concurrently with the other two machines, as it will serve as a pivot point for the next machines. The countdown timer is likely the main attack vector for this machine, as it is likely that there is something hidden in the countdown timer that can be exploited. Ironic that of course when the timer breaks, its a "zero-day" countdown AND vulnerability. 
        
        #### The Countdown Timer
        So the main breakage with the scripting of this website, and why its vulnerable. IS IN FACT THE COUNTDOWN TIMER. It calls for "someVariable" so that the countup from 2018/10/17 to the current date can be calculated. But the variable is never defined, so we can put whatever we want in there. Cross site scripting ahoy! I love writing malware and coding so much. This gift is truly a blessing. 
        
        However to make this extra efficient, i've decided to tackle this machine last after MarlinSpike specifically is popped. Then we can do a chain attack and use the reverse shell from Marlin to execute the payload on Porteus, which would be really cool. :D Two boxes at once, and a chain attack. I'm so excited.

    -- 31337 is very interesting, as it has a service tag inside of a css class. it reads:
	
	Then you'll see, that it is not the spoon that bends, it is only yourself. 
	
	The fancy graphic in the background is actually just 
	[https://youtu.be/luCYT7Qx1oA]. 
	Funny right? The obvious star in the lineup. In addition, 
	both web pages of 80 and 31337 have a countdown timer to 
	the announcement date of Matrix 4.

	-- 80 is also interesting. "Follow the White Rabbit" 
	followed by "welcome to the real world, Neo. I'm glad you're here.".
	If you follow the white rabbit, i.e. inspect the webpage 
	and open the exact html element of the center 
	graphic, its a white rabbit. The url is 
	(http://10.0.0.157/assets/img/p0rt_31337.png). 

	Path traversal is very likely.But where does the white 
	rabbit lead? It leads to the 31337 page, which is 
	interesting, as it is the same image as the 
	background of the 31337 page. 
	pages have a countdown timer to the announcement 2018/10/17 this is also interesting, as 	it is likely a hint related to that sequence. Probably the hidden service tag, which is 
	absolutely buried. Beyond that lies the assets folder 
	directory.

	-- Assets Directory: So I obviously kept following the 
	white rabbit, cause who wouldn't? Guy's in a hurry. Hidden 
	inside is .gitkeep. 
	Most likely this started as a github repository and then 
	was loaded onto the vm. Thats awesome! Gitkeep however is empty.

-- The main javascript file:

	'use strict';
	(function ($) {
		/**
	* [isMobile description]
	* @type {Object}
	*/
		window.isMobile = {
			Android: function Android() {
				return navigator.userAgent.match(/Android/i);
			},
			BlackBerry: function BlackBerry() {
				return navigator.userAgent.match(/BlackBerry/i);
			},
			iOS: function iOS() {
				return navigator.userAgent.match(/iPhone|iPad|iPod/i);
			},
			Opera: function Opera() {
				return navigator.userAgent.match(/Opera Mini/i);
			},
			Windows: function Windows() {
				return navigator.userAgent.match(/IEMobile/i);
			},
			any: function any() {
				return isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows();
			}
		};
		window.isIE = /(MSIE|Trident\/|Edge\/)/i.test(navigator.userAgent);
		window.windowHeight = window.innerHeight;
		window.windowWidth = window.innerWidth;
		if ($('#fss-bg').length) {
			var initialise = function initialise() {
				scene.add(mesh);
				scene.add(light);
				container.appendChild(renderer.element);
				window.addEventListener('resize', resize);
			};
			var resize = function resize() {
				renderer.setSize(container.offsetWidth, container.offsetHeight);
			};
			var animate = function animate() {
				now = Date.now() - start;
				light.setPosition(300 * Math.sin(now * 0.001), 200 * Math.cos(now * 0.0005), 60);
				renderer.render(scene);
				requestAnimationFrame(animate);
			};
			var container = $('#fss-bg')[0];
			var renderer = new FSS.CanvasRenderer();
			var scene = new FSS.Scene();
			var light = new FSS.Light('#111122', '#FF0022');
			var geometry = new FSS.Plane(window.innerWidth, window.innerHeight, 6, 4);
			var material = new FSS.Material('#FFFFFF', '#FFFFFF');
			var mesh = new FSS.Mesh(geometry, material);
			var now,
					start = Date.now();
			initialise();
			resize();
			animate();
		}
		var default_effect = {
			"particles": {
				"number": {
					"value": 80,
					"density": {
						"enable": true,
						"value_area": 800
					}
				},
				"color": {
					"value": "#ffffff"
				},
				"shape": {
					"type": "circle",
					"stroke": {
						"width": 0,
						"color": "#000000"
					},
					"polygon": {
						"nb_sides": 5
					}
					// "image": {
					// "src": "img/github.svg",
					// "width": 100,
					// "height": 100
					// }
				},
				"opacity": {
					"value": 0.5,
					"random": false,
					"anim": {
						"enable": false,
						"speed": 1,
						"opacity_min": 0.1,
						"sync": false
					}
				},
				"size": {
					"value": 3,
					"random": true,
					"anim": {
						"enable": false,
						"speed": 40,
						"size_min": 0.1,
						"sync": false
					}
				},
				"line_linked": {
					"enable": true,
					"distance": 150,
					"color": "#ffffff",
					"opacity": 0.4,
					"width": 1
				},
				"move": {
					"enable": true,
					"speed": 6,
					"direction": "none",
					"random": false,
					"straight": false,
					"out_mode": "out",
					"bounce": false,
					"attract": {
						"enable": false,
						"rotateX": 600,
						"rotateY": 1200
					}
				}
			},
			"interactivity": {
				"detect_on": "canvas",
				"events": {
					"onhover": {
						"enable": true,
						"mode": "repulse"
					},
					"onclick": {
						"enable": true,
						"mode": "push"
					},
					"resize": true
				},
				"modes": {
					"grab": {
						"distance": 400,
						"line_linked": {
							"opacity": 1
						}
					},
					"bubble": {
						"distance": 400,
						"size": 40,
						"duration": 2,
						"opacity": 8,
						"speed": 3
					},
					"repulse": {
						"distance": 200,
						"duration": 0.4
					},
					"push": {
						"particles_nb": 4
					},
					"remove": {
						"particles_nb": 2
					}
				}
			},
			
			"retina_detect": true
		};
		var star_effect = {
			"particles": {
				"number": {
					"value": 250,
					"density": {
						"enable": true,
						"value_area": 800
					}
				},
				"color": {
					"value": "#ffffff"
				},
				"shape": {
					"type": "circle",
					"stroke": {
						"width": 0,
						"color": "#000000"
					},
					"polygon": {
						"nb_sides": 5
					},
					"image": {
						"src": "img/github.svg",
						"width": 100,
						"height": 100
					}
				},
				"opacity": {
					"value": 0.5,
					"random": false,
					"anim": {
						"enable": false,
						"speed": 1,
						"opacity_min": 0.1,
						"sync": false
					}
				},
				"size": {
					"value": 1,
					"random": true,
					"anim": {
						"enable": true,
						"speed": 7.192807192807193,
						"size_min": 0.1,
						"sync": false
					}
				},
				"line_linked": {
					"enable": false,
					"distance": 1,
					"color": "#ffffff",
					"opacity": 0.25,
					"width": 1
				},
				"move": {
					"enable": true,
					"speed": 1,
					"direction": "none",
					"random": false,
					"straight": false,
					"out_mode": "out",
					"bounce": false,
					"attract": {
						"enable": false,
						"rotateX": 600,
						"rotateY": 1200
					}
				}
			},
			"interactivity": {
				"detect_on": "canvas",
				"events": {
					"onhover": {
						"enable": false,
						"mode": "grab"
					},
					"onclick": {
						"enable": false,
						"mode": "push"
					},
					"resize": true
				},
				"modes": {
					"grab": {
						"distance": 150,
						"line_linked": {
							"opacity": .5
						}
					},
					"bubble": {
						"distance": 400,
						"size": 40,
						"duration": 2,
						"opacity": 8,
						"speed": 3
					},
					"repulse": {
						"distance": 200,
						"duration": 0.4
					},
					"push": {
						"particles_nb": 4
					},
					"remove": {
						"particles_nb": 2
					}
				}
			},
			"retina_detect": true
		};
		var snow_effect = {
			"particles": {
				"number": {
					"value": 400,
					"density": {
						"enable": true,
						"value_area": 800
					}
				},
				"color": {
					"value": "#fff"
				},
				"shape": {
					"type": "circle",
					"stroke": {
						"width": 0,
						"color": "#000000"
					},
					"polygon": {
						"nb_sides": 5
					},
					"image": {
						"src": "img/github.svg",
						"width": 100,
						"height": 100
					}
				},
				"opacity": {
					"value": 0.5,
					"random": true,
					"anim": {
						"enable": false,
						"speed": 1,
						"opacity_min": 0.1,
						"sync": false
					}
				},
				"size": {
					"value": 10,
					"random": true,
					"anim": {
						"enable": false,
						"speed": 40,
						"size_min": 0.1,
						"sync": false
					}
				},
				"line_linked": {
					"enable": false,
					"distance": 500,
					"color": "#ffffff",
					"opacity": 0.4,
					"width": 2
				},
				"move": {
					"enable": true,
					"speed": 6,
					"direction": "bottom",
					"random": false,
					"straight": false,
					"out_mode": "out",
					"bounce": false,
					"attract": {
						"enable": false,
						"rotateX": 600,
						"rotateY": 1200
					}
				}
			},
			"interactivity": {
				"detect_on": "canvas",
				"events": {
					"onhover": {
						"enable": true,
						"mode": "bubble"
					},
					"onclick": {
						"enable": true,
						"mode": "repulse"
					},
					"resize": true
				},
				"modes": {
					"grab": {
						"distance": 400,
						"line_linked": {
							"opacity": 0.5
						}
					},
					"bubble": {
						"distance": 400,
						"size": 4,
						"duration": 0.3,
						"opacity": 1,
						"speed": 3
					},
					"repulse": {
						"distance": 200,
						"duration": 0.4
					},
					"push": {
						"particles_nb": 4
					},
					"remove": {
						"particles_nb": 2
					}
				}
			},
			"retina_detect": true
		};
		var bubble_effect = {
			"particles": {
				"number": {
					"value": 6,
					"density": {
						"enable": true,
						"value_area": 800
					}
				},
				"color": {
					"value": "#1b1e34"
				},
				"shape": {
					"type": "polygon",
					"stroke": {
						"width": 0,
						"color": "#000"
					},
					"polygon": {
						"nb_sides": 12
					},
					"image": {
						"src": "img/github.svg",
						"width": 100,
						"height": 100
					}
				},
				"opacity": {
					"value": 0.3,
					"random": true,
					"anim": {
						"enable": false,
						"speed": 1,
						"opacity_min": 0.1,
						"sync": false
					}
				},
				"size": {
					"value": 160,
					"random": false,
					"anim": {
						"enable": true,
						"speed": 10,
						"size_min": 40,
						"sync": false
					}
				},
				"line_linked": {
					"enable": false,
					"distance": 200,
					"color": "#ffffff",
					"opacity": 1,
					"width": 2
				},
				"move": {
					"enable": true,
					"speed": 8,
					"direction": "none",
					"random": false,
					"straight": false,
					"out_mode": "out",
					"bounce": false,
					"attract": {
						"enable": false,
						"rotateX": 600,
						"rotateY": 1200
					}
				}
			},
			"interactivity": {
				"detect_on": "canvas",
				"events": {
					"onhover": {
						"enable": false,
						"mode": "grab"
					},
					"onclick": {
						"enable": false,
						"mode": "push"
					},
					"resize": true
				},
				"modes": {
					"grab": {
						"distance": 400,
						"line_linked": {
							"opacity": 1
						}
					},
					"bubble": {
						"distance": 400,
						"size": 40,
						"duration": 2,
						"opacity": 8,
						"speed": 3
					},
					"repulse": {
						"distance": 200,
						"duration": 0.4
					},
					"push": {
						"particles_nb": 4
					},
					"remove": {
						"particles_nb": 2
					}
				}
			},

			"retina_detect": true
		};
		var nasa_effect = {
			"particles": {
				"number": {
					"value": 160,
					"density": {
						"enable": true,
						"value_area": 800
					}
				},
				"color": {
					"value": "#ffffff"
				},
				"shape": {
					"type": "circle",
					"stroke": {
						"width": 0,
						"color": "#000000"
					},
					"polygon": {
						"nb_sides": 5
					},
					"image": {
						"src": "img/github.svg",
						"width": 100,
						"height": 100
					}
				},
				"opacity": {
					"value": 1,
					"random": true,
					"anim": {
						"enable": true,
						"speed": 1,
						"opacity_min": 0,
						"sync": false
					}
				},
				"size": {
					"value": 3,
					"random": true,
					"anim": {
						"enable": false,
						"speed": 4,
						"size_min": 0.3,
						"sync": false
					}
				},
				"line_linked": {
					"enable": false,
					"distance": 150,
					"color": "#ffffff",
					"opacity": 0.4,
					"width": 1
				},
				"move": {
					"enable": true,
					"speed": 1,
					"direction": "none",
					"random": true,
					"straight": false,
					"out_mode": "out",
					"bounce": false,
					"attract": {
						"enable": false,
						"rotateX": 600,
						"rotateY": 600
					}
				}
			},
			"interactivity": {
				"detect_on": "canvas",
				"events": {
					"onhover": {
						"enable": true,
						"mode": "bubble"
					},
					"onclick": {
						"enable": true,
						"mode": "repulse"
					},
					"resize": true
				},
				"modes": {
					"grab": {
						"distance": 400,
						"line_linked": {
							"opacity": 1
						}
					},
					"bubble": {
						"distance": 250,
						"size": 0,
						"duration": 2,
						"opacity": 0,
						"speed": 3
					},
					"repulse": {
						"distance": 400,
						"duration": 0.4
					},
					"push": {
						"particles_nb": 4
					},
					"remove": {
						"particles_nb": 2
					}
				}
			},
			"retina_detect": true
		};

		if ($('#particles-js').length) {
			var _particles_effect = default_effect,
					_effect_data = $('#particles-js').data('effect');

			switch (_effect_data) {
				case 'star':
					_particles_effect = star_effect;
					break;
				case 'nasa':
					_particles_effect = nasa_effect;
					break;
				case 'bubble':
					_particles_effect = bubble_effect;
					break;
				case 'snow':
					_particles_effect = snow_effect;
					break;
				default:
					_particles_effect = default_effect;
			}

			particlesJS("particles-js", _particles_effect);
		}
		if ($('.quietflow').length) {
			var optData = eval('(' + $('.quietflow').attr('data-options') + ')'),
					optDefault = {
				theme: "bouncingBalls",
				specificColors: ["rgba(255, 214, 108, .5)", "rgba(192, 55, 23, .5)", "rgba(255, 153, 53, .5)", "rgba(141, 16, 12, .5)", "rgba(53, 71, 45, .5)"],
				backgroundCol: "#333"
			},
					options = $.extend(optDefault, optData);
			$("body").quietflow(options);
		}
		if ($('.ribbons-bg').length) {
			new Ribbons({
				colorSaturation: "60%",
				colorBrightness: "50%",
				colorAlpha: 0.5,
				colorCycleSpeed: 5,
				verticalPosition: "random",
				horizontalSpeed: 200,
				ribbonCount: 3,
				strokeSize: 0,
				parallaxAmount: -0.2,
				animateSections: true
			});
		}
		var smokyBG = $('#smoky-bg').waterpipe({
			gradientStart: '#51ff00',
			gradientEnd: '#001eff',
			smokeOpacity: 0.1,
			numCircles: 1,
			maxMaxRad: 'auto',
			minMaxRad: 'auto',
			minRadFactor: 0,
			iterations: 8,
			drawsPerFrame: 10,
			lineWidth: 2,
			speed: 10,
			bgColorInner: "#292929",
			bgColorOuter: "#111"
		});
		$('.vegas-container').each(function () {
			var self = $(this),
					optData = eval('(' + self.attr('data-options') + ')'),
					optDefault = {
				overlay: true,
				transition: 'fade',
				transitionDuration: 4000,
				delay: 10000,
				animation: 'random',
				animationDuration: 20000,
				slides: [{ src: 'https://picsum.photos/1000/800' }, { src: 'https://picsum.photos/1000/801' }, { src: 'https://picsum.photos/1000/802' }]
			},
					options = $.extend(optDefault, optData);
			self.vegas(options);
		});
		$(".player").mb_YTPlayer({
			showControls: false,
			ratio: 'auto',
			loop: true,
			autoPlay: true,
			mute: true
		});
		/**
	* Countdown
	*/
		$('.countdown__module').each(function () {
			var self = $(this),
					_date = self.attr('data-date'),
					_strf = self.html();
			self.countdown(_date, function (event) {
				self.html(event.strftime(_strf));
			}).removeClass("hide");
		});
	})(jQuery);

how very intriguing. After walking the available attack surface, the assets folder's other directories and listings, I have to absolutely commend the creator. Very organized, very good, very SIMPLE code that does wonders. Now to figure out how to break it. We need root for this box to be solved. 

     Vendors listed in 105:31337/assets/vendors/:
	 _jquery
	 Bootstrap
	 flat-surface-shader/
	  \  fss.min.js
     particles.js/
      \	 particles.js
	 quietflow/
	  \  quietflow.min.js
	 swiper/
	  \  swiper.min.js
	 vegas/
	  \  vegas.min.js
	 waterpipe/
	  \  waterpipe.min.js
	 mb.YTPlayer/
	  \  jquery.mb.YTPlayer.min.js

I'm learning alot about javascript for someone who mains python and dabbled in html/css. I wish I could find a typescript box and flaunt my knowledge there D:

So the main breakage with the scripting of this website, and why its vulnerable. IS IN FACT THE COUNTDOWN TIMER. It calls for "someVariable" so that the countup from 2018/10/17 to the current date can be calculated. But the variable is never defined, so we can put whatever we want in there. So if we put in a simple alert("hello world"), it will execute that code. So we can put in a simple reverse shell payload, and it will execute that code. This is the main breakage of the website, and it is likely that there is something hidden in the countdown timer that can be exploited. Ironic that of course when the timer breaks, its a "zero-day" countdown AND vulnerability.

After some brief testing, I've concluded that the best route to the next foothold is through the countdown timer, and cross-site scripting. Which is REALLY ironic since its the matrix, blending two realities as it were. Nerds. We will craft a malicious payload for the someVariable function of the countdown timer, and then execute that payload to get a reverse shell. If I get Marlin done first, I can do a chain attack and use the reverse shell from Marlin to execute the payload on Porteus, which would be really cool. :Dz

