/*global module:false*/
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    // Metadata.
    pkg: grunt.file.readJSON('package.json'),

    banner: '/*! <%= pkg.title || pkg.name %> - v<%= pkg.version %> - ' +
      '<%= grunt.template.today("yyyy-mm-dd") %>\n' +
      '<%= pkg.homepage ? "* " + pkg.homepage + "\\n" : "" %>' +
      '* Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>; */\n',

    // Task configuration.
    watch: {
      gurntfile: {
        files: 'Gruntfile.js',
        tasks: ['jshint:gruntfile'],
      },
      less: {
        files: ['assets/src/css/*.less'],
        tasks: ['recess']
      },
      javascript: {
        files: ['assets/src/js/*.js'],
        tasks: ['concat']
      }
    },

    clean: ['assets/dist'],

    copy: {
      vendor: {
        files: [
          { expand: true, cwd: 'assets/src/', src: ['js/vendor/**'], dest: 'assets/dist/' },
          { expand: true, cwd: 'assets/lib/bootstrap/', src: ['fonts/**'], dest: 'assets/dist/' }
        ]
      }
    },

    recess: {
      options: {
        compile: true,
        compress: false
      },
      bootstrap: {
        src: ['assets/lib/bootstrap/less/bootstrap.less'],
        dest: 'assets/dist/css/bootstrap.css'
      },
      theme: {
        src: ['assets/lib/bootstrap/less/theme.less'],
        dest: 'assets/dist/css/bootstrap-theme.css'
      },
      app: {
        src: ['assets/src/css/app.less'],
        dest: 'assets/dist/css/app.css'
      }
    },

    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: true
      },
      bootstrap: {
        src: [
          'assets/lib/bootstrap/js/transition.js',
          'assets/lib/bootstrap/js/alert.js',
          'assets/lib/bootstrap/js/button.js',
          'assets/lib/bootstrap/js/carousel.js',
          'assets/lib/bootstrap/js/collapse.js',
          'assets/lib/bootstrap/js/dropdown.js',
          'assets/lib/bootstrap/js/modal.js',
          'assets/lib/bootstrap/js/tooltip.js',
          'assets/lib/bootstrap/js/popover.js',
          'assets/lib/bootstrap/js/scrollspy.js',
          'assets/lib/bootstrap/js/tab.js',
          'assets/lib/bootstrap/js/affix.js'
        ],
        dest: 'assets/dist/js/bootstrap.js'
      },
      plugins: {
        src: ['assets/src/js/plugins.js', 'assets/src/js/plugins/*'],
        dest: 'assets/dist/js/plugins.js'
      },
      index: {
        src: ['assets/src/js/index.js'],
        dest: 'assets/dist/js/index.js'
      },
      home: {
        src: ['assets/src/js/home.js'],
        dest: 'assets/dist/js/home.js'
      }
    },

    uglify: {
      options: {
        banner: '<%= banner %>',
        mangle: {
          except: ['$scope']
        },
        preserveComments: false
      },
      bootstrap: {
        src: '<%= concat.bootstrap.dest %>',
        dest: '<%= concat.bootstrap.dest %>',
      },
      plugins: {
        src: '<%= concat.plugins.dest %>',
        dest: '<%= concat.plugins.dest %>',
      },
      index: {
        src: '<%= concat.index.dest %>',
        dest: '<%= concat.index.dest %>',
      },
      home: {
        src: '<%= concat.home.dest %>',
        dest: '<%= concat.home.dest %>',
      }
    },

    jshint: {
      options: {
        curly: true,
        eqeqeq: true,
        immed: true,
        latedef: true,
        newcap: true,
        noarg: true,
        sub: true,
        undef: true,
        unused: true,
        boss: true,
        eqnull: true,
        browser: true,
        globals: {}
      },
      gruntfile: {
        src: 'Gruntfile.js'
      }
    },

    connect: {
      server: {
        options: {
          keepalive: true,
          port: 5001,
          base: 'assets'
        }
      }
    }
  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-recess');

  // Default task.
  grunt.registerTask('default', ['jshint', 'clean', 'copy', 'recess', 'concat']);
  grunt.registerTask('release', ['default', 'uglify']);

};
