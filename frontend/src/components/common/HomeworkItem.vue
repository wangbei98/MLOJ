<template>
  <div style="width: 100%; margin: 20px;">
      <slot></slot>
      <!-- <b-col l="4"> -->
        <b-card
            :title="homeworkname"
            img-src="https://picsum.photos/600/300/?image=25"
            img-alt="Image"
            img-top
            tag="article"
            style="max-width: 20rem;"
            class="mb-2"
          >
            <b-card-text>
              {{homework_desc | cutString(15)}}
            </b-card-text>

            <b-button @click='clickInto' variant="primary">进入课程</b-button>
          </b-card>
      </b-col>
  </div>
</template>

<script>
  export default{
    name:'homework-item',
    props:{
      homework:{
        type:Object,
        required:true
      },
    },
    data(){
      return {
        "homeworkname": this.homework.homeworkname,
        "homework_desc": this.homework.homework_desc,
        "homework_begin_time": this.homework.homework_begin_time
      }
    },
    filters:{
      cutString(str,len){
        var reg = /[\u4e00-\u9fa5]/g,    //专业匹配中文
          slice = str.substring(0, len),
          chineseCharNum = (~~(slice.match(reg) && slice.match(reg).length)),
          realen = slice.length*2 - chineseCharNum;
        return str.substr(0, realen) + (realen < str.length ? "..." : "");
      }
    },
    computed:{
    },
    methods:{
      clickInto(){
        console.log('click into : ')
        console.log(this.homework.hid)
        this.$router.push('/homework/'+this.homework.hid)
      }
    }
  }
</script>

<style>
  .time {
      font-size: 13px;
      color: #999;
    }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    width: 100%;
    display: block;
  }
</style>
