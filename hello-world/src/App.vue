<script>
document.title = 'Picloud';
export default {
  data() {
    return {
      file: null,
      fileUrl: null
    }
  },
  methods: {
    onFileChange(e) {
      this.file = e.target.files[0];
      // this.fileUrl = URL.createObjectURL(this.file);
      // upload
      const formData = new FormData();
      formData.append('file', this.file);
      fetch('/upload', {
        method: 'POST',
        body: formData
      })
          .then(response => response.json())
          .then(data => {
            // {"src": "url","status": "ok"}
            if (data.status === 'ok') {
              this.fileUrl = "https://picloud.zh314.xyz" + data.src;
            }
            // {"error": "error message","status": "error"}
            if (data.status === 'error') {
              console.error(data.error);
            }
          })
          .catch(error => {
            console.error(error);
          });
    }
  }
}
</script>
<style>
.center {
  padding: 15% 0;
  text-align: center;
}

html {
  background-color: #2b2a33;
}


</style>
<template>

  <div id="upload" class="center">
    <h1 style="color: aliceblue;font-size: xxx-large">Picloud</h1>

    <label for="file"
           style="background-color: #42414d;color: aliceblue;padding: 10px 30px;border-radius: 5px;box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);font-size: larger">
      Choose a file</label>
    <br>
    <input type="file" id="file" @change="onFileChange" accept="image/*" style="opacity: 0;"/>
    <br>
    <div v-if="fileUrl"
         style="border-radius: 6px;border: 10px aliceblue;display: flex;width: fit-content;margin: 20px auto;align-items: center;background-color: aliceblue;box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15)">
      <span class="opblock-summary-method"
            style="background-color: #42414d;color: aliceblue;padding: 10px 30px;border-radius: 5px;font-size: larger">URL</span>
      <span style="color: black;font-size: small;padding: 10px 30px;align-items: center;white-space:nowrap;">
        {{ fileUrl }}</span>

    </div>

  </div>

</template>
