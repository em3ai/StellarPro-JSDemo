<!--
 * @Date: 2022-05-19 10:35:55
 * @LastEditTime: 2022-05-19 11:03:13
 * @Description: Modify here please
 * @FilePath: /slam-babylonjs/src/App.vue
-->
<template>
  <div id="app">
    <!-- <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div> -->
    <router-view/>
  </div>
</template>

<style lang="scss">
 html, body, div, span, applet, object, iframe,
 h1, h2, h3, h4, h5, h6, p, blockquote, pre,
 a, abbr, acronym, address, big, cite, code,
 del, dfn, em, img, ins, kbd, q, s, samp,
 small, strike, strong, sub, sup, tt, var,
 b, u, i, center,
 dl, dt, dd, ol, ul, li,
 fieldset, form, label, legend,
 table, caption, tbody, tfoot, thead, tr, th, td,
 article, aside, canvas, details, embed,
 figure, figcaption, footer, header, hgroup,
 menu, nav, output, ruby, section, summary,
 time, mark, audio, video {
   -ms-text-size-adjust: 100%;
   -webkit-text-size-adjust: 100%;
   margin: 0;
   padding: 0;
   border: 0;
   font-size: 100%;
   font: inherit;
   outline: none;
 }

body {
  margin: 0;
  overflow: hidden;
  width: 100vw;
  height: 100vh;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
  height: 100%;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
