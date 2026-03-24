document.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
        }
      });
    },
    { threshold: 0.15 }
  );

  document.querySelectorAll(".reveal").forEach((node) => observer.observe(node));

  const dropzone = document.querySelector("[data-dropzone]");
  const fileInput = document.querySelector("[data-file-input]");
  const previewFrame = document.querySelector("[data-preview-frame]");
  const previewImage = document.querySelector("[data-preview-image]");

  if (dropzone && fileInput && previewFrame && previewImage) {
    const renderPreview = (file) => {
      if (!file) {
        return;
      }
      const reader = new FileReader();
      reader.onload = (event) => {
        previewImage.src = event.target.result;
        previewFrame.classList.add("has-image");
      };
      reader.readAsDataURL(file);
    };

    fileInput.addEventListener("change", (event) => renderPreview(event.target.files[0]));

    ["dragenter", "dragover"].forEach((name) => {
      dropzone.addEventListener(name, (event) => {
        event.preventDefault();
        dropzone.classList.add("is-dragover");
      });
    });

    ["dragleave", "drop"].forEach((name) => {
      dropzone.addEventListener(name, (event) => {
        event.preventDefault();
        dropzone.classList.remove("is-dragover");
      });
    });

    dropzone.addEventListener("drop", (event) => {
      const [file] = event.dataTransfer.files;
      if (!file) {
        return;
      }
      fileInput.files = event.dataTransfer.files;
      renderPreview(file);
    });
  }

  const searchInput = document.querySelector("[data-disease-search]");
  const diseaseCards = document.querySelectorAll("[data-disease-card]");
  const emptySearch = document.querySelector("[data-empty-search]");

  if (searchInput && diseaseCards.length) {
    const applyFilter = () => {
      const query = searchInput.value.trim().toLowerCase();
      let visibleCount = 0;
      diseaseCards.forEach((card) => {
        const haystack = card.dataset.diseaseTitle || "";
        const visible = !query || haystack.includes(query);
        card.hidden = !visible;
        if (visible) {
          visibleCount += 1;
        }
      });
      if (emptySearch) {
        emptySearch.hidden = visibleCount > 0;
      }
    };

    searchInput.addEventListener("input", applyFilter);
    applyFilter();
  }
});
