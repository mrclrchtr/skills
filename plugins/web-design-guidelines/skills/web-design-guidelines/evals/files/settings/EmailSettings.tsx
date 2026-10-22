type Props = {
  email: string;
  onSave: (email: string) => Promise<void>;
};

export function EmailSettings({ email, onSave }: Props) {
  return (
    <div style={{ width: 640 }}>
      <p>Email address</p>
      <input id="email" defaultValue={email} placeholder="Email address" />
      <div onClick={() => onSave((document.getElementById("email") as HTMLInputElement).value)}>
        Save
      </div>
    </div>
  );
}
