<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-6">

    <!-- Back Button -->
    <button @click="$router.back()"
      class="mb-6 flex items-center gap-2 px-4 py-2 bg-white/70 hover:bg-white/90
             text-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all
             backdrop-blur-sm border border-gray-200">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd"
          d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
          clip-rule="evenodd"/>
      </svg>
      <span class="font-semibold">Back</span>
    </button>

    <div class="max-w-7xl mx-auto space-y-8">

      <!-- ===== HEADER + GROUP SELECTOR ===== -->
      <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
        <h1 class="text-3xl font-bold tracking-tight bg-gradient-to-r from-blue-600 to-purple-700
                   bg-clip-text text-transparent inline-block mb-2">
          Exam {{ examId }} — Analytics Dashboard
        </h1>
        <p class="text-sm text-gray-500 mb-6">
          Select <span class="font-semibold text-indigo-600">one group</span> to view its analytics,
          or <span class="font-semibold text-purple-600">multiple groups</span> to compare them side by side.
        </p>

        <!-- Group Selector Panel -->
        <div class="p-5 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl border border-indigo-200">
          <div class="flex items-center justify-between mb-3">
            <p class="text-sm font-bold text-indigo-700 uppercase tracking-wide">
              📌 Select Group(s)
            </p>
            <!-- Mode badge -->
            <div v-if="!groupsLoading && availableGroups.length > 0"
              class="flex items-center gap-2">
              <span v-if="isAllMode"
                class="px-3 py-1 text-xs font-bold rounded-full bg-blue-100 text-blue-700 border border-blue-300">
                📊 Showing: All Groups
              </span>
              <span v-else-if="selectedGroups.length === 0"
                class="px-3 py-1 text-xs font-bold rounded-full bg-amber-100 text-amber-700 border border-amber-300">
                ⚠️ No group selected
              </span>
              <span v-else-if="selectedGroups.length === 1"
                class="px-3 py-1 text-xs font-bold rounded-full bg-green-100 text-green-700 border border-green-300">
                👤 Single View
              </span>
              <span v-else
                class="px-3 py-1 text-xs font-bold rounded-full bg-purple-100 text-purple-700 border border-purple-300">
                🔀 Comparing {{ selectedGroups.length }} Groups
              </span>

              <!-- Clear selection -->
              <button v-if="selectedGroups.length > 0 && !isAllMode"
                @click="selectedGroups = []"
                class="px-3 py-1 text-xs font-semibold text-gray-500 border border-gray-300 rounded-full
                       bg-white hover:bg-gray-50 transition">
                Clear
              </button>
            </div>
          </div>

          <div v-if="groupsLoading" class="flex items-center gap-2 text-gray-500 text-sm">
            <div class="animate-spin h-4 w-4 border-2 border-indigo-500 border-t-transparent rounded-full"></div>
            Loading groups...
          </div>

          <div v-else-if="availableGroups.length === 0" class="text-sm text-gray-500 italic">
            No groups found for this exam.
          </div>

          <div v-else class="flex flex-wrap gap-3">
            <!-- ALL button -->
            <button @click="toggleAll"
              class="flex items-center gap-2 px-4 py-2 rounded-lg border-2 font-semibold text-sm transition-all"
              :class="isAllMode
                ? 'bg-blue-600 border-blue-600 text-white shadow-md'
                : 'bg-white border-gray-300 text-gray-700 hover:border-blue-400 hover:bg-blue-50'">
              <span class="w-3 h-3 rounded-full border-2 inline-flex items-center justify-center flex-shrink-0"
                :class="isAllMode ? 'border-white bg-white' : 'border-gray-400'">
                <span v-if="isAllMode" class="w-1.5 h-1.5 rounded-full bg-blue-600 inline-block"></span>
              </span>
              🌐 All Groups
            </button>

            <!-- Individual group checkboxes -->
            <button v-for="g in availableGroups" :key="g.Group_Id"
              @click="toggleGroup(g.Group_Id)"
              class="flex items-center gap-2 px-4 py-2 rounded-lg border-2 font-semibold text-sm transition-all relative"
              :class="isGroupSelected(g.Group_Id)
                ? 'border-2 text-white shadow-md'
                : 'bg-white border-gray-300 text-gray-700 hover:border-indigo-400 hover:bg-indigo-50'"
              :style="isGroupSelected(g.Group_Id) ? { backgroundColor: getGroupColor(g.Group_Id), borderColor: getGroupColor(g.Group_Id) } : {}">
              <!-- checkbox indicator -->
              <span class="w-4 h-4 rounded border-2 inline-flex items-center justify-center flex-shrink-0 transition-all"
                :class="isGroupSelected(g.Group_Id) ? 'border-white bg-white/30' : 'border-gray-400 bg-white'">
                <svg v-if="isGroupSelected(g.Group_Id)" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
              </span>
              {{ g.Group_Name }}
            </button>
          </div>

          <!-- Hint for multi-select -->
          <p v-if="selectedGroups.length >= 2" class="mt-3 text-xs text-purple-600 font-semibold">
            💡 Comparison mode: charts show each group side by side
          </p>
        </div>

        <!-- Summary Cards (single group or all) -->
        <div v-if="showSummary" class="mt-6">
          <!-- Single group summary -->
          <div v-if="!isCompareMode" class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div class="bg-gradient-to-br from-blue-50 to-blue-100 p-5 rounded-xl text-center border border-blue-200">
              <p class="text-sm font-semibold text-blue-600 mb-1">Total Attempts</p>
              <p class="text-3xl font-bold text-blue-800">{{ summaryStats.total }}</p>
            </div>
            <div class="bg-gradient-to-br from-green-50 to-green-100 p-5 rounded-xl text-center border border-green-200">
              <p class="text-sm font-semibold text-green-600 mb-1">Pass</p>
              <p class="text-3xl font-bold text-green-800">{{ summaryStats.pass }}</p>
            </div>
            <div class="bg-gradient-to-br from-red-50 to-red-100 p-5 rounded-xl text-center border border-red-200">
              <p class="text-sm font-semibold text-red-600 mb-1">Fail</p>
              <p class="text-3xl font-bold text-red-800">{{ summaryStats.fail }}</p>
            </div>
            <div class="bg-gradient-to-br from-amber-50 to-amber-100 p-5 rounded-xl text-center border border-amber-200">
              <p class="text-sm font-semibold text-amber-600 mb-1">Restricted</p>
              <p class="text-3xl font-bold text-amber-800">{{ summaryStats.restricted }}</p>
            </div>
            <div class="bg-gradient-to-br from-purple-50 to-purple-100 p-5 rounded-xl text-center border border-purple-200">
              <p class="text-sm font-semibold text-purple-600 mb-1">Avg Marks</p>
              <p class="text-3xl font-bold text-purple-800">{{ summaryStats.avg }}</p>
            </div>
          </div>

          <!-- Compare mode summary table -->
          <div v-else class="overflow-x-auto rounded-xl border border-gray-200 mt-2">
            <table class="w-full text-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="py-3 px-4 text-left text-gray-600 font-semibold">Group</th>
                  <th class="py-3 px-4 text-center text-gray-600 font-semibold">Attempts</th>
                  <th class="py-3 px-4 text-center text-gray-600 font-semibold">Pass</th>
                  <th class="py-3 px-4 text-center text-gray-600 font-semibold">Fail</th>
                  <th class="py-3 px-4 text-center text-gray-600 font-semibold">Restricted</th>
                  <th class="py-3 px-4 text-center text-gray-600 font-semibold">Avg Marks</th>
                  <th class="py-3 px-4 text-center text-gray-600 font-semibold">Pass Rate</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="gs in perGroupStats" :key="gs.groupId" class="hover:bg-gray-50">
                  <td class="py-3 px-4 font-bold flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full inline-block"
                      :style="{ backgroundColor: getGroupColor(gs.groupId) }"></span>
                    {{ gs.groupName }}
                  </td>
                  <td class="py-3 px-4 text-center font-semibold text-blue-700">{{ gs.total }}</td>
                  <td class="py-3 px-4 text-center font-semibold text-green-700">{{ gs.pass }}</td>
                  <td class="py-3 px-4 text-center font-semibold text-red-700">{{ gs.fail }}</td>
                  <td class="py-3 px-4 text-center font-semibold text-amber-700">{{ gs.restricted }}</td>
                  <td class="py-3 px-4 text-center font-semibold text-purple-700">{{ gs.avg }}</td>
                  <td class="py-3 px-4 text-center">
                    <span class="px-3 py-1 rounded-full text-xs font-bold"
                      :class="gs.passRate >= 60 ? 'bg-green-100 text-green-700' : gs.passRate >= 40 ? 'bg-amber-100 text-amber-700' : 'bg-red-100 text-red-700'">
                      {{ gs.passRate }}%
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- No selection placeholder -->
        <div v-else-if="!groupsLoading && !loading && availableGroups.length > 0"
          class="mt-6 flex flex-col items-center justify-center py-8 text-gray-400">
          <svg class="w-12 h-12 mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
          <p class="text-sm font-medium">Select a group or "All Groups" to view statistics</p>
        </div>
      </div>

      <!-- Page Loading -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-purple-600 border-t-transparent"></div>
        <span class="ml-4 text-gray-600 font-medium">Loading analytics...</span>
      </div>

      <!-- No selection — placeholder cards -->
      <template v-else-if="!showSummary">
        <div v-for="n in 2" :key="n"
          class="bg-white rounded-2xl shadow-xl border border-gray-100 p-8
                 flex flex-col items-center justify-center min-h-[260px] text-gray-400">
          <svg class="w-14 h-14 mb-4 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"/>
          </svg>
          <p class="text-base font-semibold">Select a group from above to view this chart</p>
        </div>
      </template>

      <template v-else>

        <!-- ===== CHART 1: Pass / Fail Distribution ===== -->
        <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
          <h2 class="text-xl font-bold text-gray-800 mb-1">📊 Pass / Fail Distribution</h2>
          <p class="text-sm text-gray-500 mb-6">
            {{ isCompareMode ? 'Side-by-side comparison across selected groups' : 'Overall result breakdown' }}
          </p>

          <!-- Single / All: donut pie -->
          <div v-if="!isCompareMode">
            <div v-if="chart1Data.length > 1" ref="chart1Ref" class="w-full" style="height:380px;"></div>
            <div v-else class="flex items-center justify-center h-48 text-gray-400 bg-gray-50 rounded-xl">
              No attempt data for selected group(s)
            </div>
          </div>

          <!-- Compare mode: grouped bar chart -->
          <div v-else>
            <div v-if="compareChart1Data.labels.length > 0" ref="chart1CompareRef" class="w-full" style="height:380px;"></div>
            <div v-else class="flex items-center justify-center h-48 text-gray-400 bg-gray-50 rounded-xl">
              No data to compare
            </div>
          </div>
        </div>

        <!-- ===== CHART 2: Marks Distribution ===== -->
        <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
          <h2 class="text-xl font-bold text-gray-800 mb-1">📈 Marks Distribution</h2>
          <p class="text-sm text-gray-500 mb-5">
            {{ isCompareMode ? 'Average marks comparison across groups' : 'How students scored' }}
          </p>

          <!-- Single mode controls -->
          <template v-if="!isCompareMode">
            <div class="flex gap-2 mb-5">
              <button @click="chart2Filters.viewMode = 'student'"
                :class="chart2Filters.viewMode === 'student' ? 'bg-indigo-600 text-white shadow-md' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                class="px-5 py-2 rounded-full text-sm font-semibold transition">
                👤 Student-wise
              </button>
              <button @click="chart2Filters.viewMode = 'range'"
                :class="chart2Filters.viewMode === 'range' ? 'bg-blue-600 text-white shadow-md' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                class="px-5 py-2 rounded-full text-sm font-semibold transition">
                📊 Range
              </button>
            </div>

            <div class="flex flex-wrap items-end gap-3 mb-5 p-4 bg-gray-50 rounded-xl border border-gray-200">
              <template v-if="chart2Filters.viewMode === 'range'">
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Range Size</label>
                  <div class="flex gap-1">
                    <button v-for="b in [5,10,20]" :key="b" @click="chart2Filters.bucketSize = b"
                      :class="chart2Filters.bucketSize === b ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 border border-gray-300 hover:bg-gray-100'"
                      class="px-3 py-2 rounded-lg text-sm font-semibold transition">{{ b }}</button>
                  </div>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Color Mode</label>
                  <select v-model="chart2Filters.colorMode"
                    class="px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white text-gray-700 min-w-[150px] focus:outline-none focus:ring-2 focus:ring-blue-400">
                    <option value="passfail">Pass / Fail</option>
                    <option value="score">Score %</option>
                  </select>
                </div>
              </template>

              <template v-if="chart2Filters.viewMode === 'student'">
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Sort By</label>
                  <select v-model="chart2Filters.studentSort"
                    class="px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white text-gray-700 min-w-[170px] focus:outline-none focus:ring-2 focus:ring-indigo-400">
                    <option value="marks_desc">Highest First</option>
                    <option value="marks_asc">Lowest First</option>
                    <option value="name">Name A–Z</option>
                  </select>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Color By</label>
                  <select v-model="chart2Filters.colorMode"
                    class="px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white text-gray-700 min-w-[150px] focus:outline-none focus:ring-2 focus:ring-indigo-400">
                    <option value="passfail">Pass / Fail</option>
                    <option value="score">Score %</option>
                  </select>
                </div>
              </template>

              <div class="flex flex-col gap-1">
                <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Avg Line</label>
                <label class="flex items-center gap-2 cursor-pointer px-3 py-2 rounded-lg border border-gray-300 bg-white">
                  <input type="checkbox" v-model="chart2Filters.showAvgLine" class="w-4 h-4 accent-purple-600"/>
                  <span class="text-sm text-gray-700">Show Avg</span>
                </label>
              </div>
              <button @click="clearChart2Filters"
                class="px-4 py-2 text-sm bg-white border border-gray-300 text-gray-600 rounded-lg hover:bg-gray-100 transition self-end">
                Clear
              </button>
            </div>

            <div v-if="chart2Filters.showAvgLine && chart2Avg > 0"
              class="mb-4 inline-flex items-center gap-2 px-4 py-2 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700 font-medium">
              <span class="w-6 h-0.5 bg-red-500 inline-block rounded"></span>
              Average: {{ chart2Avg }} marks
            </div>

            <div v-if="chart2SingleData.rows && chart2SingleData.rows.length > 0" ref="chart2Ref" class="w-full"></div>
            <div v-else class="flex items-center justify-center h-48 text-gray-400 bg-gray-50 rounded-xl">
              No data available
            </div>
          </template>

          <!-- Compare mode: avg marks per group + range overlay -->
          <template v-else>
            <!-- Compare mode sub-toggle -->
            <div class="flex gap-2 mb-5">
              <button @click="chart2CompareMode = 'avg'"
                :class="chart2CompareMode === 'avg' ? 'bg-purple-600 text-white shadow-md' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                class="px-5 py-2 rounded-full text-sm font-semibold transition">
                📊 Avg Marks
              </button>
              <button @click="chart2CompareMode = 'range'"
                :class="chart2CompareMode === 'range' ? 'bg-blue-600 text-white shadow-md' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                class="px-5 py-2 rounded-full text-sm font-semibold transition">
                🔢 Score Range
              </button>
              <button @click="chart2CompareMode = 'passfail'"
                :class="chart2CompareMode === 'passfail' ? 'bg-green-600 text-white shadow-md' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                class="px-5 py-2 rounded-full text-sm font-semibold transition">
                ✅ Pass/Fail %
              </button>
            </div>

            <div ref="chart2CompareRef" class="w-full" style="height:380px;"></div>
          </template>
        </div>

      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import axios from '../utils/axiosInstance'

const route  = useRoute()
const examId = route.params.examId

// ─── Raw Data ──────────────────────────────────────────────────────────────
const attempts         = ref([])
const applicantMap     = ref({})      // applicantId → Group_Id (number)
const applicantNameMap = ref({})      // applicantId → Full_Name
const loading          = ref(true)
const groupsLoading    = ref(true)
const maxMarks         = ref(100)

// ─── Chart Refs ────────────────────────────────────────────────────────────
const chart1Ref        = ref(null)
const chart1CompareRef = ref(null)
const chart2Ref        = ref(null)
const chart2CompareRef = ref(null)
const chartsReady      = ref(false)

// ─── Group Selection ───────────────────────────────────────────────────────
const allLoadedGroups = ref([])    // all groups fetched from API
const selectedGroups  = ref([])    // array of Group_Id numbers (multi-select)
const isAllMode       = ref(false)
const chart2CompareMode = ref('avg')   // 'avg' | 'range' | 'passfail'

// Only show groups that have at least 1 attempt in this exam
const availableGroups = computed(() => {
  if (!attempts.value.length) return allLoadedGroups.value
  const groupsWithData = new Set(
    attempts.value
      .map(a => Number(applicantMap.value[a.Applicant_Id]))
      .filter(gid => gid && !isNaN(gid))
  )
  return allLoadedGroups.value.filter(g => groupsWithData.has(Number(g.Group_Id)))
})

// Group color palette for comparison
const GROUP_COLORS = [
  '#6366f1', '#22c55e', '#f59e0b', '#ef4444',
  '#14b8a6', '#8b5cf6', '#ec4899', '#0ea5e9',
  '#84cc16', '#f97316'
]
function getGroupColor(groupId) {
  const idx = availableGroups.value.findIndex(g => g.Group_Id === groupId)
  return GROUP_COLORS[idx % GROUP_COLORS.length]
}

function toggleAll() {
  isAllMode.value = !isAllMode.value
  if (isAllMode.value) selectedGroups.value = []
}

function toggleGroup(groupId) {
  if (isAllMode.value) isAllMode.value = false
  const idx = selectedGroups.value.indexOf(groupId)
  if (idx === -1) selectedGroups.value.push(groupId)
  else selectedGroups.value.splice(idx, 1)
}

function isGroupSelected(groupId) {
  return selectedGroups.value.includes(groupId)
}

// ─── Modes ─────────────────────────────────────────────────────────────────
const isCompareMode = computed(() => !isAllMode.value && selectedGroups.value.length >= 2)
const showSummary   = computed(() => isAllMode.value || selectedGroups.value.length > 0)

// ─── Filtered attempts ─────────────────────────────────────────────────────
// Returns all attempts for the active selection (all groups or selected group ids)
const activeAttempts = computed(() => {
  if (isAllMode.value) return attempts.value
  if (selectedGroups.value.length === 0) return []
  const set = new Set(selectedGroups.value.map(Number))
  return attempts.value.filter(a => set.has(Number(applicantMap.value[a.Applicant_Id])))
})

// Attempts per group (used for compare mode)
function attemptsForGroup(groupId) {
  return attempts.value.filter(a => Number(applicantMap.value[a.Applicant_Id]) === Number(groupId))
}

// ─── Summary Stats ─────────────────────────────────────────────────────────
function computeStats(list) {
  const total = list.length
  const pass  = list.filter(a => a.Status === 'Pass').length
  const fail  = list.filter(a => a.Status === 'Fail').length
  const restricted = list.filter(a => a.Status === 'Restricted').length
  const valid = list.filter(a => a.Marks_Obtained != null)
  const avg   = valid.length
    ? (valid.reduce((s, a) => s + parseFloat(a.Marks_Obtained || 0), 0) / valid.length).toFixed(1)
    : '0.0'
  const passRate = total > 0 ? Math.round((pass / total) * 100) : 0
  return { total, pass, fail, restricted, avg, passRate }
}

const summaryStats = computed(() => computeStats(activeAttempts.value))

const perGroupStats = computed(() => {
  const groups = isAllMode.value
    ? availableGroups.value
    : availableGroups.value.filter(g => selectedGroups.value.includes(g.Group_Id))
  return groups.map(g => ({
    groupId:   g.Group_Id,
    groupName: g.Group_Name,
    ...computeStats(attemptsForGroup(g.Group_Id))
  }))
})

// ─── Chart 2 Avg ───────────────────────────────────────────────────────────
const chart2Avg = computed(() => {
  const list = activeAttempts.value.filter(a => a.Marks_Obtained != null)
  if (!list.length) return 0
  return parseFloat((list.reduce((s, a) => s + parseFloat(a.Marks_Obtained || 0), 0) / list.length).toFixed(1))
})

// ─── Chart 2 Filters ───────────────────────────────────────────────────────
const chart2Filters = ref({
  viewMode: 'student', bucketSize: 10,
  showAvgLine: false, colorMode: 'passfail', studentSort: 'marks_desc'
})

function clearChart2Filters() {
  chart2Filters.value = {
    viewMode: chart2Filters.value.viewMode, bucketSize: 10,
    showAvgLine: false, colorMode: 'passfail', studentSort: 'marks_desc'
  }
}

// ─── Chart 1 Data (single / all) ───────────────────────────────────────────
const chart1Data = computed(() => {
  const f = activeAttempts.value
  const rows = [['Status', 'Count']]
  const pass = f.filter(a => a.Status === 'Pass').length
  const fail = f.filter(a => a.Status === 'Fail').length
  const rest = f.filter(a => a.Status === 'Restricted').length
  if (pass > 0) rows.push(['Pass', pass])
  if (fail > 0) rows.push(['Fail', fail])
  if (rest > 0) rows.push(['Restricted', rest])
  return rows
})

// ─── Chart 1 Compare Data ──────────────────────────────────────────────────
const compareChart1Data = computed(() => {
  const groups = isAllMode.value
    ? availableGroups.value
    : availableGroups.value.filter(g => selectedGroups.value.includes(g.Group_Id))

  // DataTable format: Group | Pass | Fail | Restricted
  const rows = [['Group', 'Pass', 'Fail', 'Restricted']]
  groups.forEach(g => {
    const list = attemptsForGroup(g.Group_Id)
    rows.push([
      g.Group_Name,
      list.filter(a => a.Status === 'Pass').length,
      list.filter(a => a.Status === 'Fail').length,
      list.filter(a => a.Status === 'Restricted').length,
    ])
  })
  return { labels: groups.map(g => g.Group_Name), rows }
})

// ─── Chart 2 Single Data ───────────────────────────────────────────────────
const chart2SingleData = computed(() => {
  const f2   = chart2Filters.value
  const list = activeAttempts.value

  if (f2.viewMode === 'student') {
    let sorted = [...list]
    if (f2.studentSort === 'marks_desc')
      sorted.sort((a, b) => parseFloat(b.Marks_Obtained || 0) - parseFloat(a.Marks_Obtained || 0))
    else if (f2.studentSort === 'marks_asc')
      sorted.sort((a, b) => parseFloat(a.Marks_Obtained || 0) - parseFloat(b.Marks_Obtained || 0))
    else
      sorted.sort((a, b) => {
        const na = applicantNameMap.value[a.Applicant_Id] || a.Student_Email || ''
        const nb = applicantNameMap.value[b.Applicant_Id] || b.Student_Email || ''
        return na.localeCompare(nb)
      })

    const rows = sorted.map(a => {
      const marks = parseFloat(a.Marks_Obtained || 0)
      const pct   = maxMarks.value > 0 ? (marks / maxMarks.value) * 100 : 0
      const name  = applicantNameMap.value[a.Applicant_Id]
        || (a.Student_Email || '').split('@')[0]
        || `ID:${a.Applicant_Id}`
      const grpColor = getGroupColor(Number(applicantMap.value[a.Applicant_Id]))
      let color = '#6366f1'
      if (f2.colorMode === 'passfail')
        color = a.Status === 'Pass' ? '#22c55e' : a.Status === 'Restricted' ? '#f59e0b' : '#ef4444'
      else
        color = pct < 30 ? '#ef4444' : pct < 60 ? '#f59e0b' : '#22c55e'
      // In all-group mode, outline by group color
      return { name, email: a.Student_Email || '', marks, status: a.Status, color, grpColor }
    })
    return { rows, mode: 'student' }
  }

  // Range mode
  const bs = parseInt(f2.bucketSize)
  const lo = 0, hi = maxMarks.value
  if (!list.length) return { rows: [], mode: 'range' }
  const buckets = {}
  for (let s = lo; s < hi; s += bs) buckets[s] = 0
  list.forEach(a => {
    const m  = parseFloat(a.Marks_Obtained || 0)
    const bk = Math.floor((m - lo) / bs) * bs + lo
    const key = Math.max(lo, Math.min(bk, hi - bs))
    if (buckets[key] !== undefined) buckets[key]++
  })
  const rows = Object.entries(buckets).map(([start, count]) => {
    const s   = parseInt(start)
    const pct = ((s + bs / 2) / hi) * 100
    const color = f2.colorMode === 'score'
      ? (pct < 30 ? '#ef4444' : pct < 60 ? '#f59e0b' : '#22c55e')
      : ((s + bs / 2) >= hi * 0.4 ? '#22c55e' : '#ef4444')
    return { label: `${s}–${s + bs - 1}`, count, color }
  })
  return { rows, mode: 'range' }
})

// ─── Chart 2 Compare Data ──────────────────────────────────────────────────
const compareChart2Data = computed(() => {
  const groups = isAllMode.value
    ? availableGroups.value
    : availableGroups.value.filter(g => selectedGroups.value.includes(g.Group_Id))

  if (chart2CompareMode.value === 'avg') {
    // Bar: group → avg marks
    const rows = [['Group', 'Avg Marks', { role: 'style' }, { role: 'annotation' }]]
    groups.forEach(g => {
      const list  = attemptsForGroup(g.Group_Id).filter(a => a.Marks_Obtained != null)
      const avg   = list.length
        ? parseFloat((list.reduce((s, a) => s + parseFloat(a.Marks_Obtained || 0), 0) / list.length).toFixed(1))
        : 0
      rows.push([g.Group_Name, avg, getGroupColor(g.Group_Id), avg.toString()])
    })
    return rows

  } else if (chart2CompareMode.value === 'passfail') {
    // Grouped bar: Group | Pass% | Fail%
    const rows = [['Group', 'Pass %', 'Fail %', 'Restricted %']]
    groups.forEach(g => {
      const list = attemptsForGroup(g.Group_Id)
      const total = list.length || 1
      rows.push([
        g.Group_Name,
        Math.round((list.filter(a => a.Status === 'Pass').length / total) * 100),
        Math.round((list.filter(a => a.Status === 'Fail').length / total) * 100),
        Math.round((list.filter(a => a.Status === 'Restricted').length / total) * 100),
      ])
    })
    return rows

  } else {
    // Score range: stacked bar per group
    // Bands: 0-40, 40-70, 70-100
    const rows = [['Group', '0–39 (Low)', '40–69 (Mid)', '70–100 (High)']]
    groups.forEach(g => {
      const list = attemptsForGroup(g.Group_Id)
      const hi = maxMarks.value || 100
      const low = list.filter(a => (parseFloat(a.Marks_Obtained) / hi) * 100 < 40).length
      const mid = list.filter(a => { const p = (parseFloat(a.Marks_Obtained) / hi) * 100; return p >= 40 && p < 70 }).length
      const high = list.filter(a => (parseFloat(a.Marks_Obtained) / hi) * 100 >= 70).length
      rows.push([g.Group_Name, low, mid, high])
    })
    return rows
  }
})

// ─── Google Charts ─────────────────────────────────────────────────────────
function loadGoogleCharts() {
  return new Promise(resolve => {
    if (window.google && window.google.visualization) { resolve(); return }
    const script = document.createElement('script')
    script.src = 'https://www.gstatic.com/charts/loader.js'
    script.onload = () => {
      window.google.charts.load('current', { packages: ['corechart', 'bar'] })
      window.google.charts.setOnLoadCallback(resolve)
    }
    document.head.appendChild(script)
  })
}

// ─── Draw Chart 1 ──────────────────────────────────────────────────────────
function drawChart1() {
  if (!chartsReady.value) return

  if (!isCompareMode.value) {
    // Donut pie
    if (!chart1Ref.value || chart1Data.value.length <= 1) return
    const data = window.google.visualization.arrayToDataTable(chart1Data.value)
    new window.google.visualization.PieChart(chart1Ref.value).draw(data, {
      pieHole: 0.45,
      colors: ['#22c55e', '#ef4444', '#f59e0b'],
      legend: { position: 'right', textStyle: { fontSize: 14 } },
      chartArea: { width: '80%', height: '80%' },
      pieSliceText: 'percentage',
      pieSliceTextStyle: { fontSize: 14, bold: true },
      backgroundColor: 'transparent',
    })
  } else {
    // Grouped column chart per group
    if (!chart1CompareRef.value || compareChart1Data.value.rows.length < 2) return
    const data = window.google.visualization.arrayToDataTable(compareChart1Data.value.rows)
    new window.google.visualization.ColumnChart(chart1CompareRef.value).draw(data, {
      isStacked: false,
      colors: ['#22c55e', '#ef4444', '#f59e0b'],
      legend: { position: 'top', textStyle: { fontSize: 13 } },
      chartArea: { width: '75%', height: '70%' },
      hAxis: { textStyle: { fontSize: 12 } },
      vAxis: { title: 'Students', minValue: 0, format: '#', textStyle: { fontSize: 11 } },
      backgroundColor: 'transparent',
      bar: { groupWidth: '60%' },
    })
  }
}

// ─── Draw Chart 2 ──────────────────────────────────────────────────────────
function drawChart2() {
  if (!chartsReady.value) return

  if (!isCompareMode.value) {
    // Single / All mode
    if (!chart2Ref.value) return
    const d2 = chart2SingleData.value
    if (!d2.rows || !d2.rows.length) return

    if (d2.mode === 'student') {
      const dataArray = [['Student', 'Marks', { role: 'style' }, { role: 'annotation' }, { role: 'tooltip', p: { html: true } }]]
      d2.rows.forEach(r => {
        dataArray.push([
          r.name.length > 20 ? r.name.substring(0, 18) + '…' : r.name,
          r.marks, r.color, r.marks.toString(),
          `<div style="padding:8px 12px;font-size:13px;line-height:1.6">
            <b>${r.name}</b><br>
            <span style="color:#6b7280;font-size:11px">${r.email}</span><br>
            Marks: <b>${r.marks}</b> / ${maxMarks.value}<br>
            Status: <b style="color:${r.color}">${r.status}</b>
          </div>`
        ])
      })
      chart2Ref.value.style.height = Math.max(280, d2.rows.length * 28 + 80) + 'px'
      new window.google.visualization.BarChart(chart2Ref.value).draw(
        window.google.visualization.arrayToDataTable(dataArray), {
          legend: { position: 'none' },
          chartArea: { width: '60%', height: '90%' },
          hAxis: { title: 'Marks', minValue: 0, maxValue: maxMarks.value, textStyle: { fontSize: 11 } },
          vAxis: { textStyle: { fontSize: 11 } },
          bar: { groupWidth: 16 },
          backgroundColor: 'transparent',
          annotations: { alwaysOutside: true, textStyle: { fontSize: 10, bold: true, color: '#374151' } },
          tooltip: { isHtml: true, trigger: 'focus' }
        }
      )
    } else {
      chart2Ref.value.style.height = '320px'
      const dataArray = [['Range', 'Students', { role: 'style' }, { role: 'annotation' }]]
      d2.rows.forEach(r => dataArray.push([r.label, r.count, r.color, r.count.toString()]))
      new window.google.visualization.ColumnChart(chart2Ref.value).draw(
        window.google.visualization.arrayToDataTable(dataArray), {
          legend: { position: 'none' },
          chartArea: { width: '78%', height: '72%' },
          hAxis: { title: 'Marks Range', textStyle: { fontSize: 12 } },
          vAxis: { title: 'Students', minValue: 0, format: '#' },
          bar: { groupWidth: '45%' },
          backgroundColor: 'transparent',
          annotations: { alwaysOutside: true, textStyle: { fontSize: 12, bold: true } },
        }
      )
    }
  } else {
    // Compare mode
    if (!chart2CompareRef.value) return
    const rows = compareChart2Data.value
    if (!rows || rows.length <= 1) return
    const data = window.google.visualization.arrayToDataTable(rows)

    if (chart2CompareMode.value === 'avg') {
      new window.google.visualization.ColumnChart(chart2CompareRef.value).draw(data, {
        legend: { position: 'none' },
        chartArea: { width: '75%', height: '72%' },
        hAxis: { textStyle: { fontSize: 12 } },
        vAxis: { title: 'Avg Marks', minValue: 0, maxValue: maxMarks.value, textStyle: { fontSize: 11 } },
        bar: { groupWidth: '50%' },
        backgroundColor: 'transparent',
        annotations: { alwaysOutside: true, textStyle: { fontSize: 12, bold: true, color: '#374151' } },
      })
    } else if (chart2CompareMode.value === 'passfail') {
      new window.google.visualization.ColumnChart(chart2CompareRef.value).draw(data, {
        isStacked: false,
        colors: ['#22c55e', '#ef4444', '#f59e0b'],
        legend: { position: 'top', textStyle: { fontSize: 13 } },
        chartArea: { width: '75%', height: '68%' },
        hAxis: { textStyle: { fontSize: 12 } },
        vAxis: { title: 'Percentage (%)', minValue: 0, maxValue: 100, textStyle: { fontSize: 11 } },
        bar: { groupWidth: '60%' },
        backgroundColor: 'transparent',
      })
    } else {
      // Score range stacked
      new window.google.visualization.ColumnChart(chart2CompareRef.value).draw(data, {
        isStacked: true,
        colors: ['#ef4444', '#f59e0b', '#22c55e'],
        legend: { position: 'top', textStyle: { fontSize: 13 } },
        chartArea: { width: '75%', height: '68%' },
        hAxis: { textStyle: { fontSize: 12 } },
        vAxis: { title: 'Students', minValue: 0, format: '#', textStyle: { fontSize: 11 } },
        bar: { groupWidth: '55%' },
        backgroundColor: 'transparent',
      })
    }
  }
}

// ─── Redraw all ────────────────────────────────────────────────────────────
function redrawAll() {
  nextTick(() => { drawChart1(); drawChart2() })
}

// ─── Watchers ──────────────────────────────────────────────────────────────
watch([selectedGroups, isAllMode],       redrawAll, { deep: true })
watch(chart1Data,                        () => nextTick(drawChart1), { deep: true })
watch([chart2Filters, chart2SingleData, () => chart2Avg.value], () => nextTick(drawChart2), { deep: true })
watch(chart2CompareMode,                 () => nextTick(drawChart2))
watch(compareChart1Data,                 () => nextTick(drawChart1), { deep: true })
watch(compareChart2Data,                 () => nextTick(drawChart2), { deep: true })

// ─── onMounted ─────────────────────────────────────────────────────────────
onMounted(async () => {
  const email = localStorage.getItem('email')
  const role  = localStorage.getItem('active_role')

  try {
    // 1. Attempts
    const res = await axios.get('/attempts', { params: { exam_id: examId, email, role } })
    if (res.data.success) {
      attempts.value = res.data.attempts
      const marks = attempts.value.map(a => parseFloat(a.Max_Marks || 0)).filter(m => m > 0)
      if (marks.length) maxMarks.value = Math.max(...marks)
    }

    // 2. Load ALL groups (needed to build complete applicant→group map)
    try {
      const gRes = await axios.get('/groups', { params: { role, email, show_all: 'true' } })
      if (gRes.data.success) {
        allLoadedGroups.value = (gRes.data.groups || []).map(g => ({
          Group_Id: g.Group_Id, Group_Name: g.Group_Name
        }))
      }
    } catch {}

    // 3. Build applicant→group and name maps for ALL groups
    for (const g of allLoadedGroups.value) {
      try {
        const aRes = await axios.get(`/groups/${g.Group_Id}/applicants`)
        if (aRes.data.success) {
          ;(aRes.data.applicants || []).forEach(a => {
            applicantMap.value[a.Applicant_Id]     = g.Group_Id
            applicantNameMap.value[a.Applicant_Id] = a.Full_Name || a.Name || null
          })
        }
      } catch {}
    }
    // NOTE: availableGroups is a computed that filters allLoadedGroups
    // to only those with actual attempt data — so the selector only
    // shows groups where students have submitted the exam.

  } finally {
    loading.value       = false
    groupsLoading.value = false
  }

  await loadGoogleCharts()
  chartsReady.value = true
})
</script>

<style scoped>
.bg-clip-text { -webkit-background-clip: text; background-clip: text; }
</style>