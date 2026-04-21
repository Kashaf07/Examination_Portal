<template>
  <div class="relative group" style="width:48px;height:48px;">
    <!-- Avatar -->
    <div
      class="w-12 h-12 rounded-full overflow-hidden flex items-center justify-center font-bold text-white shadow-md cursor-pointer select-none"
      :style="profilePicUrl ? '' : 'background:linear-gradient(135deg,#3b82f6,#6366f1)'"
      @click="profilePicUrl ? onBadgeClick($event) : triggerFileInput()"
      title="Click to change profile picture"
    >
      <img v-if="profilePicUrl" :src="profilePicUrl" alt="Profile" class="w-full h-full object-cover"
           @error="profilePicUrl = null; localStorage.removeItem('profile_pic_path'); localStorage.removeItem('profile_pic_url')" />
      <span v-else class="text-base">{{ initial }}</span>
    </div>

    <!-- + badge -->
    <div
      class="absolute w-5 h-5 bg-blue-600 rounded-full flex items-center justify-center cursor-pointer border-2 border-white shadow-md"
      :class="{ 'badge-pop': !profilePicUrl }"
      style="bottom:0px; right:-4px;"
      @click.stop="onBadgeClick"
      title="Profile picture options"
    >
      <svg class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="3">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
      </svg>
    </div>

    <input ref="fileInput" type="file" accept="image/jpeg,image/jpg,image/png,image/webp" class="hidden" @change="onFileSelected" />

    <!-- Context menu (only when pic exists) -->
    <teleport to="body">
      <div
        v-if="showMenu"
        class="context-menu"
        :style="{ top: menuPos.y + 'px', left: menuPos.x + 'px' }"
        @click.stop
      >
        <button class="menu-item" @click="onEditClick">
          <svg class="menu-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536M9 13l6.586-6.586a2 2 0 112.828 2.828L11.828 15.828A2 2 0 0110 16H8v-2a2 2 0 01.586-1.414z" />
          </svg>
          Edit
        </button>
        <div class="menu-divider"></div>
        <button class="menu-item menu-item-danger" @click="onDeleteClick">
          <svg class="menu-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7h6m2 0a1 1 0 00-1-1h-4a1 1 0 00-1 1H5" />
          </svg>
          Delete
        </button>
      </div>
    </teleport>

    <!-- Crop Modal -->
    <teleport to="body">
      <div
        v-if="showCropModal"
        class="fixed inset-0 z-[9999] flex items-center justify-center"
        style="background:rgba(0,0,0,0.72);backdrop-filter:blur(4px);"
      >
        <div class="bg-white rounded-2xl shadow-2xl flex flex-col" style="width:520px;max-width:95vw;">
          <!-- Header -->
          <div class="px-6 pt-5 pb-3 border-b border-gray-100">
            <h3 class="text-lg font-bold text-gray-900">Crop Profile Photo</h3>
            <p class="text-sm text-gray-500 mt-0.5">Drag to reposition · Use edge handles to resize</p>
          </div>

          <!-- Canvas area -->
          <div class="px-6 py-5 flex items-center justify-center bg-gray-900" style="min-height:340px;">
            <div
              ref="canvasWrap"
              class="relative overflow-hidden select-none"
              :style="{ width: displayW + 'px', height: displayH + 'px' }"
            >
              <!-- Image -->
              <img
                ref="imgEl"
                :src="rawImageSrc"
                alt=""
                class="absolute top-0 left-0 pointer-events-none"
                :style="{ width: displayW + 'px', height: displayH + 'px', objectFit: 'contain' }"
                draggable="false"
              />

              <!-- Dark overlays (4 sides around crop square) -->
              <div class="absolute left-0 right-0 top-0 pointer-events-none overlay-dark" :style="{ height: crop.y + 'px' }"></div>
              <div class="absolute left-0 right-0 pointer-events-none overlay-dark" :style="{ top: (crop.y + crop.size) + 'px', bottom: 0 }"></div>
              <div class="absolute pointer-events-none overlay-dark" :style="{ top: crop.y + 'px', height: crop.size + 'px', left: 0, width: crop.x + 'px' }"></div>
              <div class="absolute pointer-events-none overlay-dark" :style="{ top: crop.y + 'px', height: crop.size + 'px', left: (crop.x + crop.size) + 'px', right: 0 }"></div>

              <!-- Circular outline -->
              <div
                class="absolute rounded-full pointer-events-none crop-ring"
                :style="{ left: crop.x + 'px', top: crop.y + 'px', width: crop.size + 'px', height: crop.size + 'px' }"
              ></div>

              <!-- Draggable crop area -->
              <div
                class="absolute"
                :style="{ left: crop.x + 'px', top: crop.y + 'px', width: crop.size + 'px', height: crop.size + 'px', cursor: 'move' }"
                @mousedown.stop="startMove"
              >
                <!-- Rule of thirds (inside circle clip) -->
                <div class="absolute inset-0 pointer-events-none" style="border-radius:50%;overflow:hidden;">
                  <div class="absolute bg-white/15" style="left:33.33%;top:0;bottom:0;width:1px;"></div>
                  <div class="absolute bg-white/15" style="left:66.66%;top:0;bottom:0;width:1px;"></div>
                  <div class="absolute bg-white/15" style="top:33.33%;left:0;right:0;height:1px;"></div>
                  <div class="absolute bg-white/15" style="top:66.66%;left:0;right:0;height:1px;"></div>
                </div>

                <!-- Top edge handle -->
                <div class="edge-handle-zone" style="top:-6px;left:50%;transform:translateX(-50%);cursor:n-resize;" @mousedown.stop="startResize('t',$event)">
                  <div class="handle-pill horizontal"></div>
                </div>
                <!-- Bottom edge handle -->
                <div class="edge-handle-zone" style="bottom:-6px;left:50%;transform:translateX(-50%);cursor:s-resize;" @mousedown.stop="startResize('b',$event)">
                  <div class="handle-pill horizontal"></div>
                </div>
                <!-- Left edge handle -->
                <div class="edge-handle-zone" style="left:-6px;top:50%;transform:translateY(-50%);cursor:w-resize;" @mousedown.stop="startResize('l',$event)">
                  <div class="handle-pill vertical"></div>
                </div>
                <!-- Right edge handle -->
                <div class="edge-handle-zone" style="right:-6px;top:50%;transform:translateY(-50%);cursor:e-resize;" @mousedown.stop="startResize('r',$event)">
                  <div class="handle-pill vertical"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Preview + Actions -->
          <div class="px-6 py-4 flex items-center justify-between border-t border-gray-100">
            <div class="flex items-center gap-3">
              <canvas ref="previewCanvas" width="56" height="56" class="rounded-full border-2 border-gray-200 shadow-sm" style="width:56px;height:56px;"></canvas>
              <span class="text-xs text-gray-400">Preview</span>
            </div>
            <div class="flex gap-3">
              <button @click="cancelCrop" class="px-5 py-2 rounded-xl border border-gray-300 text-gray-600 font-semibold text-sm hover:bg-gray-50 transition">
                Cancel
              </button>
              <button @click="confirmCrop" :disabled="uploading"
                class="px-6 py-2 rounded-xl bg-blue-600 text-white font-semibold text-sm hover:bg-blue-700 transition disabled:opacity-60 flex items-center gap-2">
                <svg v-if="uploading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                </svg>
                {{ uploading ? 'Saving...' : 'Apply' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </teleport>

    <!-- Delete confirm modal -->
    <teleport to="body">
      <div
        v-if="showDeleteConfirm"
        class="fixed inset-0 z-[9999] flex items-center justify-center"
        style="background:rgba(0,0,0,0.5);backdrop-filter:blur(3px);"
      >
        <div class="bg-white rounded-2xl shadow-2xl p-6 flex flex-col items-center gap-4" style="width:320px;max-width:90vw;">
          <div class="w-14 h-14 rounded-full bg-blue-50 flex items-center justify-center">
            <svg class="w-7 h-7 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7h6m2 0a1 1 0 00-1-1h-4a1 1 0 00-1 1H5" />
            </svg>
          </div>
          <div class="text-center">
            <h3 class="text-base font-bold text-gray-900">Remove Profile Photo?</h3>
            <p class="text-sm text-gray-500 mt-1">This will permanently remove your profile picture.</p>
          </div>
          <div class="flex gap-3 w-full">
            <button @click="showDeleteConfirm = false" class="flex-1 px-4 py-2 rounded-xl border border-gray-300 text-gray-600 font-semibold text-sm hover:bg-gray-50 transition">
              Cancel
            </button>
            <button @click="confirmDelete" :disabled="uploading" class="flex-1 px-4 py-2 rounded-xl bg-blue-600 text-white font-semibold text-sm hover:bg-blue-700 transition disabled:opacity-60">
              {{ uploading ? 'Removing...' : 'Remove' }}
            </button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import axiosInstance from '@/utils/axiosInstance'

const props = defineProps({ initial: { type: String, default: '?' } })
const emit = defineEmits(['updated'])

const fileInput      = ref(null)
const showCropModal  = ref(false)
const showDeleteConfirm = ref(false)
const showMenu       = ref(false)
const menuPos        = ref({ x: 0, y: 0 })
const rawImageSrc    = ref('')
const profilePicUrl  = ref(null)
const uploading      = ref(false)

const imgEl          = ref(null)
const canvasWrap     = ref(null)
const previewCanvas  = ref(null)

// Always render a 300×300 square display area
const DISPLAY_SIZE = 300
const displayW = ref(DISPLAY_SIZE)
const displayH = ref(DISPLAY_SIZE)

// Natural image dimensions
const natW = ref(0)
const natH = ref(0)

// Crop state: always a square (x, y, size)
const crop = ref({ x: 0, y: 0, size: 200 })
const MIN_SIZE = 60

// ─── Build URL from filename (no timestamp — file is replaced on upload, not renamed) ───
function buildPicUrl(path) {
  const filename = path.replace('profile_pics/', '')
  return `http://${window.location.hostname}:5000/api/profile/pic-file/${filename}`
}
function getRenderedBounds() {
  const imgAspect = natW.value / natH.value
  let offX = 0, offY = 0, rendW = displayW.value, rendH = displayH.value
  if (imgAspect > 1) {
    rendH = displayW.value / imgAspect
    offY = (displayH.value - rendH) / 2
  } else {
    rendW = displayH.value * imgAspect
    offX = (displayW.value - rendW) / 2
  }
  return { offX, offY, rendW, rendH }
}

// ─── Reset crop: fill as much of the image as possible, centered ───
function resetCrop() {
  const { offX, offY, rendW, rendH } = getRenderedBounds()
  const size = Math.min(rendW, rendH)
  crop.value = {
    x: offX + (rendW - size) / 2,
    y: offY + (rendH - size) / 2,
    size,
  }
}

// ─── Badge click handler ───
function onBadgeClick(e) {
  if (profilePicUrl.value) {
    const rect = e.currentTarget.getBoundingClientRect()
    menuPos.value = {
      x: rect.left + window.scrollX - 50,
      y: rect.bottom + window.scrollY + 8,
    }
    showMenu.value = !showMenu.value
  } else {
    triggerFileInput()
  }
}

function onEditClick() {
  showMenu.value = false
  triggerFileInput()
}

function onDeleteClick() {
  showMenu.value = false
  showDeleteConfirm.value = true
}

async function confirmDelete() {
  uploading.value = true
  try {
    await axiosInstance.delete('/profile/delete-pic')
    profilePicUrl.value = null
    localStorage.removeItem('profile_pic_path')
    localStorage.removeItem('profile_pic_url')
    emit('updated', null)
  } catch (err) {
    alert('Delete failed: ' + (err.response?.data?.error || err.message))
  } finally {
    uploading.value = false
    showDeleteConfirm.value = false
  }
}

// ─── File input ───
function triggerFileInput() { fileInput.value?.click() }

function onFileSelected(e) {
  const file = e.target.files[0]
  if (!file) return

  const allowed = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
  if (!allowed.includes(file.type)) {
    alert('Only JPG, PNG, or WEBP images are allowed.')
    e.target.value = ''
    return
  }
  const reader = new FileReader()
  reader.onload = (ev) => {
    rawImageSrc.value = ev.target.result
    const img = new Image()
    img.onload = async () => {
      natW.value = img.naturalWidth
      natH.value = img.naturalHeight
      displayW.value = DISPLAY_SIZE
      displayH.value = DISPLAY_SIZE
      showCropModal.value = true
      await nextTick()
      resetCrop()
      updatePreview()
    }
    img.src = ev.target.result
  }
  reader.readAsDataURL(file)
  e.target.value = ''
}

// ─── Move crop box ───
let moving = false
let moveStart = { mx: 0, my: 0, cx: 0, cy: 0 }

function startMove(e) {
  moving = true
  moveStart = { mx: e.clientX, my: e.clientY, cx: crop.value.x, cy: crop.value.y }
  window.addEventListener('mousemove', onMoveMove)
  window.addEventListener('mouseup', onMoveUp)
}

function onMoveMove(e) {
  if (!moving) return
  const dx = e.clientX - moveStart.mx
  const dy = e.clientY - moveStart.my
  const { offX, offY, rendW, rendH } = getRenderedBounds()
  crop.value.x = Math.min(Math.max(moveStart.cx + dx, offX), offX + rendW - crop.value.size)
  crop.value.y = Math.min(Math.max(moveStart.cy + dy, offY), offY + rendH - crop.value.size)
  updatePreview()
}

function onMoveUp() {
  moving = false
  window.removeEventListener('mousemove', onMoveMove)
  window.removeEventListener('mouseup', onMoveUp)
}

// ─── Resize — edge handles only, always keeps square ───
let resizing = false
let resizeEdge = ''
let resizeStart = {}

function startResize(edge, e) {
  resizing = true
  resizeEdge = edge
  resizeStart = { mx: e.clientX, my: e.clientY, ...crop.value }
  window.addEventListener('mousemove', onResizeMove)
  window.addEventListener('mouseup', onResizeUp)
}

function onResizeMove(e) {
  if (!resizing) return
  const dx = e.clientX - resizeStart.mx
  const dy = e.clientY - resizeStart.my
  const { offX, offY, rendW, rendH } = getRenderedBounds()

  let { x, y, size } = resizeStart

  if (resizeEdge === 't') {
    // drag up = grow (delta is negative dy), drag down = shrink
    const newSize = Math.max(MIN_SIZE, size - dy)
    y = y + (size - newSize)          // anchor bottom edge
    size = newSize
  } else if (resizeEdge === 'b') {
    size = Math.max(MIN_SIZE, size + dy)  // anchor top edge
  } else if (resizeEdge === 'l') {
    const newSize = Math.max(MIN_SIZE, size - dx)
    x = x + (size - newSize)          // anchor right edge
    size = newSize
  } else if (resizeEdge === 'r') {
    size = Math.max(MIN_SIZE, size + dx)  // anchor left edge
  }

  // Clamp within rendered image
  x = Math.max(offX, x)
  y = Math.max(offY, y)
  if (x + size > offX + rendW) size = offX + rendW - x
  if (y + size > offY + rendH) size = offY + rendH - y
  size = Math.max(MIN_SIZE, size)

  crop.value = { x, y, size }
  updatePreview()
}

function onResizeUp() {
  resizing = false
  window.removeEventListener('mousemove', onResizeMove)
  window.removeEventListener('mouseup', onResizeUp)
}

// ─── Preview canvas ───
function updatePreview() {
  if (!previewCanvas.value || !imgEl.value) return
  const ctx = previewCanvas.value.getContext('2d')
  const { offX, offY, rendW, rendH } = getRenderedBounds()
  const scaleX = natW.value / rendW
  const scaleY = natH.value / rendH

  const sx = (crop.value.x - offX) * scaleX
  const sy = (crop.value.y - offY) * scaleY
  const sw = crop.value.size * scaleX
  const sh = crop.value.size * scaleY

  ctx.clearRect(0, 0, 56, 56)
  ctx.beginPath()
  ctx.arc(28, 28, 28, 0, Math.PI * 2)
  ctx.clip()
  ctx.drawImage(imgEl.value, sx, sy, sw, sh, 0, 0, 56, 56)
}

// ─── Cancel ───
function cancelCrop() {
  showCropModal.value = false
  rawImageSrc.value = ''
}

// ─── Confirm & Upload ───
async function confirmCrop() {
  uploading.value = true
  try {
    const OUTPUT = 400
    const canvas = document.createElement('canvas')
    canvas.width = OUTPUT
    canvas.height = OUTPUT
    const ctx = canvas.getContext('2d')

    const { offX, offY, rendW, rendH } = getRenderedBounds()
    const scaleX = natW.value / rendW
    const scaleY = natH.value / rendH

    const sx = (crop.value.x - offX) * scaleX
    const sy = (crop.value.y - offY) * scaleY
    const sw = crop.value.size * scaleX
    const sh = crop.value.size * scaleY

    const img = new Image()
    img.src = rawImageSrc.value
    await new Promise(r => { img.onload = r; if (img.complete) r() })
    ctx.drawImage(img, sx, sy, sw, sh, 0, 0, OUTPUT, OUTPUT)

    const blob = await new Promise(r => canvas.toBlob(r, 'image/jpeg', 0.92))
    const formData = new FormData()
    formData.append('profile_pic', blob, 'profile.jpg')

    const res = await axiosInstance.post('/profile/upload-pic', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    if (res.data.success) {
      const path = res.data.profile_pic
      const url = buildPicUrl(path)
      profilePicUrl.value = url
      localStorage.setItem('profile_pic_path', path)
      emit('updated', url)
      showCropModal.value = false
    } else {
      alert('Upload failed: ' + (res.data.error || 'Unknown error'))
    }
  } catch (err) {
    console.error('Upload error:', err)
    alert('Upload failed:\n' + (err.response?.data?.error || err.response?.data?.traceback || err.message))
  } finally {
    uploading.value = false
  }
}

// ─── Close menu on outside click ───
function handleOutsideClick() { showMenu.value = false }

// ─── Load existing pic on mount ───
onMounted(async () => {
  // Restore from localStorage immediately using stored path — no token needed
  const cachedPath = localStorage.getItem('profile_pic_path')
  if (cachedPath) profilePicUrl.value = buildPicUrl(cachedPath)

  try {
    const res = await axiosInstance.get('/profile/get-pic')
    if (res.data.profile_pic) {
      const path = res.data.profile_pic
      profilePicUrl.value = buildPicUrl(path)
      localStorage.setItem('profile_pic_path', path)
    } else {
      // Backend confirmed no pic — clear cache
      profilePicUrl.value = null
      localStorage.removeItem('profile_pic_path')
      localStorage.removeItem('profile_pic_url')
    }
  } catch (e) {
    // Token expired or network error — keep showing cached pic, it loads directly without auth
  }

  document.addEventListener('click', handleOutsideClick)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', onMoveMove)
  window.removeEventListener('mouseup', onMoveUp)
  window.removeEventListener('mousemove', onResizeMove)
  window.removeEventListener('mouseup', onResizeUp)
  document.removeEventListener('click', handleOutsideClick)
})
</script>

<style scoped>
/* ─── Badge pop animation ─── */
@keyframes badge-pop {
  0%   { transform: scale(1);    box-shadow: 0 0 0 0   rgba(59,130,246,0.7); }
  50%  { transform: scale(1.25); box-shadow: 0 0 0 6px rgba(59,130,246,0);   }
  100% { transform: scale(1);    box-shadow: 0 0 0 0   rgba(59,130,246,0);   }
}
.badge-pop { animation: badge-pop 1.8s ease-in-out infinite; }

/* ─── Dark overlay ─── */
.overlay-dark { background: rgba(0,0,0,0.55); }

/* ─── Circular crop ring ─── */
.crop-ring {
  border: 2px solid rgba(255,255,255,0.88);
  box-shadow: 0 0 0 1px rgba(0,0,0,0.25);
}

/* ─── Edge handles ─── */
.edge-handle-zone {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
}

.handle-pill {
  background: #ffffff;
  border-radius: 99px;
  box-shadow: 0 1px 5px rgba(0,0,0,0.4);
}
.handle-pill.horizontal { width: 38px; height: 5px; }
.handle-pill.vertical   { width: 5px;  height: 38px; }

/* ─── Context menu ─── */
.context-menu {
  position: fixed;
  z-index: 99999;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.16), 0 2px 8px rgba(0,0,0,0.08);
  padding: 6px;
  min-width: 130px;
  animation: menu-in 0.14s cubic-bezier(0.2,0,0,1.2);
}

@keyframes menu-in {
  from { opacity: 0; transform: scale(0.88) translateY(-6px); }
  to   { opacity: 1; transform: scale(1)    translateY(0);    }
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 12px;
  border: none;
  background: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: background 0.12s;
}
.menu-item:hover          { background: #f3f4f6; }
.menu-item-danger         { color: #ef4444; }
.menu-item-danger:hover   { background: #fef2f2; }

.menu-icon { width: 15px; height: 15px; flex-shrink: 0; }

.menu-divider { height: 1px; background: #f3f4f6; margin: 4px 0; }
</style>