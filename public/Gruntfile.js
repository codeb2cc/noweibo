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
        files: ['src/css/*.less'],
        tasks: ['recess']
      },
      javascript: {
        files: ['src/js/*.js'],
        tasks: ['concat']
      }
    },

    clean: ['assets/dist'],

    copy: {
      vendor: {
        files: [
          { expand: true, cwd: 'src/', src: ['js/vendor/**'], dest: 'dist/' },
          { expand: true, cwd: 'src/lib/bootstrap/', src: ['fonts/**'], dest: 'dist/' }
        ]
      }
    },

    recess: {
      options: { compile: true },
      dev: {
        options: { compress: false },
        files: {
          'dist/css/bootstrap.css': 'src/lib/bootstrap/less/bootstrap.less',
          'dist/css/bootstrap-theme.css': 'src/lib/bootstrap/less/theme.less',
          'dist/css/app.css': 'src/css/app.less'
        }
      },
      release: {
        options: { compress: true },
        files: {
          'dist/css/bootstrap.css': 'src/lib/bootstrap/less/bootstrap.less',
          'dist/css/bootstrap-theme.css': 'src/lib/bootstrap/less/theme.less',
          'dist/css/app.css': 'src/css/app.less'
        }
      }
    },

    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: true
      },
      bootstrap: {
        src: [
          'src/lib/bootstrap/js/transition.js',
          'src/lib/bootstrap/js/alert.js',
          'src/lib/bootstrap/js/button.js',
          'src/lib/bootstrap/js/carousel.js',
          'src/lib/bootstrap/js/collapse.js',
          'src/lib/bootstrap/js/dropdown.js',
          'src/lib/bootstrap/js/modal.js',
          'src/lib/bootstrap/js/tooltip.js',
          'src/lib/bootstrap/js/popover.js',
          'src/lib/bootstrap/js/scrollspy.js',
          'src/lib/bootstrap/js/tab.js',
          'src/lib/bootstrap/js/affix.js'
        ],
        dest: 'dist/js/bootstrap.js'
      },
      plugins: {
        src: ['src/js/plugins.js', 'src/js/plugins/*'],
        dest: 'dist/js/plugins.js'
      },
      index: {
        src: ['src/js/index.js'],
        dest: 'dist/js/index.js'
      },
      home: {
        src: ['src/js/home.js'],
        dest: 'dist/js/home.js'
      }
    },

    uglify: {
      options: {
        banner: '<%= banner %>',
        mangle: {
          except: ['$scope', '$http', '$timeout']
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
          base: '.'
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
  grunt.registerTask('default', ['jshint', 'clean', 'copy', 'recess:dev', 'concat']);
  grunt.registerTask('release', ['jshint', 'clean', 'copy', 'recess:release', 'concat', 'uglify']);

};
