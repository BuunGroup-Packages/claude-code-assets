# Pagination & Streaming

## Auto-Pagination

```typescript
async *listAutoPaging(params?: ListUsersParams): AsyncIterable<User> {
  let cursor = params?.after;
  do {
    const page = await this.list({ ...params, after: cursor });
    for (const item of page.data) {
      yield item;
    }
    cursor = page.next_cursor ?? undefined;
  } while (cursor);
}

// Usage
for await (const user of client.users.listAutoPaging({ role: 'admin' })) {
  console.log(user.name);
}
```

## Server-Sent Events (SSE) Streaming

```typescript
const stream = client.messages
  .stream({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 1024,
    messages: [{ role: 'user', content: 'Hello' }],
  })
  .on('text', (text) => process.stdout.write(text))
  .on('error', (error) => console.error(error));

const finalMessage = await stream.finalMessage();
```
