var playlist = Vue.extend({
    data: function(){
          return {
              show: false,
          };
    },
    props: ['name','songs'],
    template: '#playlist',
    delimiters: ['[[',']]'],
    methods: {
        popup: function(event){
            this.show = !this.show;
        },
        getSong: function(song){
            this.$parent.getS(song.id);
            this.$parent.$data.play = false;
            this.$parent.$data.currentSong = this.songs.indexOf(song);
        }
    },
    computed: {
        count: function(){
            return this.songs.length;
        },
    },
});

//Vue.component('playlist',playlist);

var app = new Vue({
    el: '.player',
    data: {
        songs: [],
        play: false,
        showDetail: false,
        currentPlayList: 'all',
        currentSong: 0,
    }, 
    delimiters: ['[[',']]'],
    components: {
        'playlist': playlist,
    },
    computed: {
    },
    methods: {
        popup: function(){
            this.show = !this.show;
        },
        getS: function(id){
            this.$http.get('/getSong/'+id).then(function(res){
              document.getElementById('control-hidden').src = '/get/source/' + res.data.song[0][2];
              document.getElementsByClassName('song-pic')[0].src = '/get/pic/' + res.data.song[0][3];
			  var u = 'url(/get/pic/' + res.data.song[0][3] + ')'
			console.log(u);
              document.getElementsByClassName('disk')[0].style.backgroundImage = u;
			  console.log(document.getElementsByClassName('disk')[0].style.backgroundImage);
              document.getElementsByClassName('song-title')[0].innerText = res.data.song[0][0];
              document.getElementsByClassName('song-title')[1].innerText = res.data.song[0][0];
              document.getElementsByClassName('song-singer')[0].innerText = res.data.song[0][1];
            },fail);
        },           
        toggle: function(){
            this.play = !this.play;
            if(this.play){
                document.getElementById('control-hidden').play();
                document.getElementsByClassName('disk')[0].className = 'disk rotate';
            }
            else{
                document.getElementById('control-hidden').pause();
                document.getElementsByClassName('disk')[0].className = 'disk';
            }
        },
        progress: function(){
            setInterval(function(){
                var currentTime = document.getElementById('control-hidden').currentTime;
                var duration = document.getElementById('control-hidden').duration;
                var bgw = parseInt(document.getElementsByClassName('bg-bar')[0].offsetWidth);
                document.getElementsByClassName('progress-bar')[0].style.width = (currentTime*bgw)/duration + 'px';
            },1000);
        },
        adjust: function(event){
            var bgw = parseInt(document.getElementsByClassName('bg-bar')[0].offsetWidth);
            var duration = document.getElementById('control-hidden').duration;
            var x = event.offsetX;
            document.getElementById('control-hidden').currentTime = x*duration/bgw;
            document.getElementsByClassName('progress-bar')[0].style.width = x + 'px';
        },
        prev: function(){
            var isplay = this.play;
            var len = this.$refs.all.songs.length;
            this.currentSong = (this.currentSong - 1) % len;
            if (this.currentSong === -1){
                this.currentSong = len-1;
            }
            var id = this.$refs.all.songs[this.currentSong].id;
            this.getS(id);
            this.play = false;
            document.getElementById('control-hidden').addEventListener('canplay',play,false);
        },            
        next: function(){
            var isplay = this.play;
            var len = this.$refs.all.songs.length;
            this.currentSong = (this.currentSong + 1) % len;
            var id = this.$refs.all.songs[this.currentSong].id;
            this.getS(id);
            this.play = false;
            document.getElementById('control-hidden').addEventListener('canplay',play,false);
        },            
    },
    mounted: function(){
        this.$http.get('/getSongs').then(function(res){
            this.songs = transform(res.data.songs);
            id = this.songs[0].id;
            this.getS(id);
        },fail);
        this.progress();
        var that = this;
        document.getElementById('control-hidden').onended = function(){
            that.next();
        };       
    },
});

function fail(){
    console.log('fail');
}

function transform(data){
    var res = [];
    for(var i = 0; i < data.length; i++){
        res.push({id: data[i][0],title: data[i][1],singer: data[i][2]});
    }
    return res;
}

function play(event){
    var pl = event.target;
    pl.play();
    app.$data.play = true;
    pl.removeEventListener('canplay',play,false);
} 
