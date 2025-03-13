import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert embed_dim % num_heads == 0

        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        self.qkv_proj = nn.Linear(embed_dim, embed_dim * 3)
        self.output_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x):
        batch_size, seq_length, embed_dim = x.size()
        qkv = self.qkv_proj(x).reshape(batch_size, seq_length, self.num_heads, 3 * self.head_dim)
        q, k, v = qkv.chunk(3, dim=-1)

        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)

        attn_weights = F.softmax(torch.matmul(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5), dim=-1)
        attn_output = torch.matmul(attn_weights, v)

        attn_output = attn_output.transpose(1, 2).reshape(batch_size, seq_length, embed_dim)
        return self.output_proj(attn_output)

class GroupedQueryAttention(nn.Module):
    def __init__(self, embed_dim, num_heads, num_groups):
        super(GroupedQueryAttention, self).__init__()
        assert num_heads % num_groups == 0

        self.num_heads = num_heads
        self.num_groups = num_groups
        self.head_dim = embed_dim // num_heads

        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.kv_proj = nn.Linear(embed_dim, embed_dim * 2 // num_groups)
        self.output_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x):
        batch_size, seq_length, embed_dim = x.size()

        q = self.q_proj(x).reshape(batch_size, seq_length, self.num_heads, self.head_dim).transpose(1, 2)
        kv = self.kv_proj(x).reshape(batch_size, seq_length, self.num_groups, 2 * self.head_dim).transpose(1, 2)
        k, v = kv.chunk(2, dim=-1)

        group_size = self.num_heads // self.num_groups
        k = k.repeat_interleave(group_size, dim=1)  # 注意这里是repeat_interleave而不是repeat!前者将[1,2]变成[1,1,1,2,2,2];后者将[1,2]变成[1,2,1,2,1,2]
        v = v.repeat_interleave(group_size, dim=1)

        attn_weights = F.softmax(torch.matmul(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5), dim=-1)
        attn_output = torch.matmul(attn_weights, v)

        attn_output = attn_output.transpose(1, 2).reshape(batch_size, seq_length, embed_dim)
        return self.output_proj(attn_output)

# 示例用法
embed_dim = 64
num_heads = 8
num_groups = 4

x = torch.randn(32, 10, embed_dim)

mha = MultiHeadAttention(embed_dim, num_heads)
gha = GroupedQueryAttention(embed_dim, num_heads, num_groups)

mha_output = mha(x)
gha_output = gha(x)

print(mha_output.shape)  # 输出: (32, 10, 64)
print(gha_output.shape)  # 输出: (32, 10, 64)
