# Godot C# API Reference for AI Agents

> Quick-reference for common Godot C# patterns used in agentic development.
> Assumes Godot 4.4+, .NET build.

---

## Node Lifecycle (Override Order)

```csharp
public partial class MyNode : Node
{
    // Called when node enters the scene tree (parent assigned, children NOT yet ready)
    public override void _EnterTree() { }

    // Called when all children have entered the scene tree (ready for init)
    public override void _Ready() { }

    // Called every frame (delta = seconds since last frame)
    public override void _Process(double delta) { }

    // Called every physics tick (default 60 FPS, stable delta)
    public override void _PhysicsProcess(double delta) { }

    // Called when node exits the scene tree
    public override void _ExitTree() { }
}
```

### Common Base Classes

| Class | Purpose | Key Features |
|-------|---------|--------------|
| `Node` | Base for everything | Scene tree ops, signals, groups |
| `Node2D` | 2D game objects | Position, rotation, scale, transforms |
| `Control` | UI elements | Rect size, anchors, layout, theme |
| `CharacterBody2D` | Movable 2D character | `MoveAndSlide()`, collision handling |
| `Area2D` | Detection zone | `BodyEntered`, `AreaEntered` signals |
| `RigidBody2D` | Physics-simulated body | Forces, torque, mass, friction |
| `Sprite2D` | 2D visual | Texture, flip, modulate colour |
| `AnimationPlayer` | Play animations | Timeline-based property animation |
| `TileMap` | Tile-based grids | Cell queries, layer management |

---

## Scene Tree Operations

```csharp
// Get a child by name (common, returns null if missing)
var player = GetNode<CharacterBody2D>("Player");

// Get by path relative to this node
var hud = GetNode<Control>("UI/HUD");

// Get root node (the scene root)
var root = GetNode<Node>("/root");

// Get the owning scene's root
var sceneRoot = GetTree().CurrentScene;

// Find a node anywhere in the tree
var enemy = GetTree().GetFirstNodeInGroup("enemies");

// Check if a node is valid before use
if (IsInstanceValid(player))
    player.Position = Vector2.Zero;

// Add/remove from scene tree
AddChild(newSprite);
RemoveChild(oldNode);
oldNode.QueueFree();           // Schedules deletion at end of frame
oldNode.QueueFree();           // idempotent — safe to call multiple times
```

---

## Signals (Godot's Event System)

```csharp
// === Declaration (at class level) ===
[Signal]
public delegate void HealthChangedEventHandler(float oldHealth, float newHealth);

[Signal]
public delegate void DeathEventHandler();

// === Emission (inside method) ===
EmitSignal(SignalName.HealthChanged, currentHealth, newHealth);
EmitSignal(SignalName.Death);

// === Connection ===
// In _Ready or a setup method:
player.HealthChanged += OnPlayerHealthChanged;
player.Death += OnPlayerDeath;

// One-shot connection (disconnects after first fire):
player.HealthChanged += () => GD.Print("First health change!");

// === One-shot (built-in Godot 4.x) ===
player.HealthChanged += Callable.From((float oldHp, float newHp) =>
    GD.Print($"{oldHp} → {newHp}")
);
```

---

## Properties & Exports

```csharp
// === Export fields (editable in inspector) ===
[Export]
public float Speed { get; set; } = 300.0f;

[Export]
public PackedScene BulletScene { get; set; }

[Export]
public Godot.Collections.Array<Texture2D> Animations { get; set; }

// === Export groups (inspector organisation) ===
[ExportGroup("Combat")]
[Export]
public int MaxHealth { get; set; } = 100;
[Export]
public int AttackDamage { get; set; } = 10;
[ExportGroup("Movement")]
[Export]
public float JumpVelocity { get; set; } = -400.0f;
[ExportGroup("")]  // End group

// === Export enums ===
public enum AttackType { Melee, Ranged, Magic }
[Export]
public AttackType CurrentAttack { get; set; }

// === Property with setter-side-effect ===
private float _health;
[Export]
public float Health
{
    get => _health;
    set
    {
        _health = Mathf.Clamp(value, 0, MaxHealth);
        if (_health <= 0)
            EmitSignal(SignalName.Death);
    }
}
```

---

## Input Handling

```csharp
// Check action state (every frame in _Process)
public override void _Process(double delta)
{
    Vector2 direction = Input.GetVector("move_left", "move_right", "move_up", "move_down");
    Position += direction * Speed * (float)delta;
}

// Single-press detection
public override void _UnhandledInput(InputEvent @event)
{
    if (Input.IsActionJustPressed("jump"))
        Jump();

    if (Input.IsActionJustReleased("shoot"))
        Shoot();
}

// Mouse position
public override void _UnhandledInput(InputEvent @event)
{
    if (@event is InputEventMouseButton mouseBtn && mouseBtn.ButtonIndex == MouseButton.Left)
    {
        Vector2 clickPos = GetGlobalMousePosition();
        GD.Print($"Clicked at: {clickPos}");
    }
}
```

---

## Resource Management

```csharp
// Load resources (returns null on failure)
var texture = GD.Load<Texture2D>("res://assets/player.png");
var scene = GD.Load<PackedScene>("res://scenes/enemy.tscn");

// Instantiate a scene
var enemy = scene.Instantiate<Node2D>();
AddChild(enemy);

// Preload at compile time (similar to const-assert)
[Export]
public PackedScene ProjectilePrefab { get; set; }  // Assign in inspector

// Resource as C# object — create and save at runtime
var res = new Resource();
res.SetMeta("author", "Agent");
ResourceSaver.Save(res, "res://generated/agent_data.tres");

// Access project settings
float gravity = (float)ProjectSettings.GetSetting("physics/2d/default_gravity");
```

---

## C#-Specific Patterns

### Partial Classes (Godot Requirement)

```csharp
// Every scriptable Godot node must be a partial class
// The other half is generated by Godot from the .uid file
public partial class Player : CharacterBody2D { }
```

### Async / Await with Godot

```csharp
// Wait for a signal
await ToSignal(GetTree().CreateTimer(2.0f), Timer.SignalName.Timeout);
GD.Print("2 seconds elapsed");

// Wait for a custom signal
await ToSignal(player, Player.SignalName.Death);
GD.Print("Player died");

// Wait for next physics frame
await ToSignal(GetTree(), SceneTree.SignalName.PhysicsFrame);
```

### Godot-Specific Types

```csharp
Vector2  = (x, y)                    // 2D position, size, velocity
Vector3  = (x, y, z)                 // 3D position
Color    = (r, g, b, a) or #RRGGBB
Transform2D = (rotation, scale, position)
Rect2    = (position, size)          // AABB
StringName                            // Interned string for signal/group names
Godot.Collections.Array / Dictionary   // Use these for [Export] collections
```

### Nullable Reference Types

```csharp
#nullable enable
public partial class Weapon : Node
{
    private Player? _owner;  // explicit nullable

    public void Equip(Player owner)
    {
        _owner = owner;
    }

    public void Attack()
    {
        if (_owner == null) return;
        // safe to use _owner here
    }
}
```

---

## Common Pitfalls (C# in Godot)

| Pitfall | Explanation | Fix |
|---------|-------------|-----|
| `GetNode<T>` returns null silently | If path is wrong, no error until dereference | Always null-check or use `GetNodeOrNull<T>` |
| `.cs` script not attached | Godot won't pick up changes until `dotnet build` | Always rebuild after C# edits |
| `[Signal]` delegate return type is `void` | Signals cannot return values | Use method chaining instead |
| `Mathf` vs `Math` | Godot uses `Mathf`, not System.Math | `Mathf.Sqrt`, `Mathf.Sin`, etc. |
| `float` vs `double` in delta | `_Process(double delta)` — cast if needed | `(float)delta` |
| UID changes | Moving .cs files externally breaks references | Run `update_project_uids()` or let Godot rebuild |
| Exported fields lose values after rename | Godot tracks by name + type | Use `[ExportProperty]` or manual migration |
