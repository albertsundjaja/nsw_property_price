<script setup>
import ModelClient from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";
import { ref, onMounted } from 'vue';

const csvContent = ref('')
const prompt = ref('')
const aiResponse = ref('')
const token = ref('')
const tempToken = ref('')

const sendPrompt = async () => {
  try {
    const client = new ModelClient(
        "https://models.inference.ai.azure.com",
        new AzureKeyCredential(token.value)
    );

    const response = await client.path("/chat/completions").post({
        body: {
            messages: [
                { role: "system", content: "You are a real estate agent" },
                { role: "system", content: "You have this raw data about NSW property prices" },
                { role: "system", content: csvContent.value },
                { role: "user", content: prompt.value },
            ],
            model: "gpt-4o-mini",
            temperature: 1,
            max_tokens: 4096,
            top_p: 1
        }
    });

    if (response.status !== "200") {
        throw response.body.error;
    }
    aiResponse.value = response.body.choices[0].message.content;
  } catch (error) {
    aiResponse.value = 'Error fetching response'
  }
}

function saveToken() {
  if (tempToken.value) {
    token.value = tempToken.value; // Save the token
    tempToken.value = ''; // Clear the temporary input
  } else {
    alert('Please enter a valid GitHub token.');
  }
}

async function loadCsv() {
  try {
    const response = await fetch('raw_data/summary.csv');
    if (!response.ok) {
      throw new Error('Failed to load CSV file');
    }
    csvContent.value = await response.text();
  } catch (error) {
    console.error(error);
  }
}

// Automatically load the CSV when the component is mounted
onMounted(() => {
  loadCsv();
});
</script>

<template>
  <v-app>
    <v-main>
      <v-container>
        <v-row>
          <v-col cols="12">
            <h1>NSW Property Price Chat</h1>
          </v-col>
        </v-row>
        <!-- Token Input Section -->
        <v-row v-if="!token">
          <v-col cols="12">
            <v-text-field
              label="To interact with the AI, please enter your GitHub Token"
              v-model="tempToken"
              type="password"
              hint="Your token will be used to authenticate requests"
              variant="outlined"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-btn size="large" color="primary" @click="saveToken">Submit Token</v-btn>
          </v-col>
        </v-row>

        <!-- Chat Interface -->
        <v-row v-else>
          <v-col cols="12">
            <div>
              <v-text-field
                label="Enter your prompt"
                hint="try asking &quot;What's the most expensive suburb?&quot;"
                variant="outlined"
                v-model="prompt"
              ></v-text-field>
            </div>
          </v-col>
          <v-col cols="12">
            <v-btn size="large" color="primary" @click="sendPrompt">Query</v-btn>
          </v-col>
          <v-col cols="12">
            <v-card v-if="aiResponse">
              <v-card-text>
                <pre>{{ aiResponse }}</pre>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>