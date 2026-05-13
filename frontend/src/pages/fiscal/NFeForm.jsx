import { Save } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { createNFe, listFiscalCompanies, listFiscalCustomers, listFiscalProducts, listOperationNatures } from '../../services/fiscalService.js'

const emptyItem = { produto: '', quantidade: '1.0000', valor_unitario: '0.00', desconto: '0.00' }

export function NFeForm() {
  const navigate = useNavigate()
  const [companies, setCompanies] = useState([])
  const [customers, setCustomers] = useState([])
  const [products, setProducts] = useState([])
  const [natures, setNatures] = useState([])
  const [form, setForm] = useState({
    numero: '',
    serie: '1',
    tipo_operacao: 'venda',
    emitente: '',
    destinatario_cliente: '',
    natureza_operacao: '',
    valor_frete: '0.00',
    valor_desconto: '0.00',
    itens: [emptyItem],
  })
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    Promise.all([listFiscalCompanies(), listFiscalCustomers(), listFiscalProducts(), listOperationNatures()]).then(([companyRows, customerRows, productRows, natureRows]) => {
      setCompanies(companyRows)
      setCustomers(customerRows)
      setProducts(productRows)
      setNatures(natureRows)
    })
  }, [])

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  function updateItem(field, value) {
    setForm((current) => ({ ...current, itens: [{ ...current.itens[0], [field]: value }] }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSaving(true)
    const payload = {
      ...form,
      numero: Number(form.numero),
      serie: Number(form.serie),
      emitente: Number(form.emitente),
      destinatario_cliente: Number(form.destinatario_cliente),
      natureza_operacao: Number(form.natureza_operacao),
      itens: form.itens.map((item) => ({ ...item, produto: Number(item.produto) })),
    }
    const nota = await createNFe(payload)
    navigate(`/fiscal/nfe/${nota.id}`)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Fiscal</p>
        <h2 className="text-2xl font-semibold text-slate-950">Nova NF-e</h2>
      </div>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-4">
        <FormField label="Numero">
          <input className={inputClassName} value={form.numero} onChange={(event) => updateField('numero', event.target.value)} required />
        </FormField>
        <FormField label="Serie">
          <input className={inputClassName} value={form.serie} onChange={(event) => updateField('serie', event.target.value)} required />
        </FormField>
        <FormField label="Emitente">
          <select className={inputClassName} value={form.emitente} onChange={(event) => updateField('emitente', event.target.value)} required>
            <option value="">Selecione</option>
            {companies.map((company) => <option key={company.id} value={company.id}>{company.razao_social}</option>)}
          </select>
        </FormField>
        <FormField label="Natureza">
          <select className={inputClassName} value={form.natureza_operacao} onChange={(event) => updateField('natureza_operacao', event.target.value)} required>
            <option value="">Selecione</option>
            {natures.map((nature) => <option key={nature.id} value={nature.id}>{nature.codigo}</option>)}
          </select>
        </FormField>
        <FormField label="Cliente fiscal">
          <select className={inputClassName} value={form.destinatario_cliente} onChange={(event) => updateField('destinatario_cliente', event.target.value)} required>
            <option value="">Selecione</option>
            {customers.map((customer) => <option key={customer.cliente} value={customer.cliente}>{customer.cpf_cnpj}</option>)}
          </select>
        </FormField>
        <FormField label="Frete">
          <input className={inputClassName} value={form.valor_frete} onChange={(event) => updateField('valor_frete', event.target.value)} />
        </FormField>
        <FormField label="Desconto">
          <input className={inputClassName} value={form.valor_desconto} onChange={(event) => updateField('valor_desconto', event.target.value)} />
        </FormField>
      </section>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-4">
        <FormField label="Produto fiscal">
          <select className={inputClassName} value={form.itens[0].produto} onChange={(event) => updateItem('produto', event.target.value)} required>
            <option value="">Selecione</option>
            {products.map((product) => <option key={product.produto} value={product.produto}>{product.produto_nome}</option>)}
          </select>
        </FormField>
        <FormField label="Quantidade">
          <input className={inputClassName} value={form.itens[0].quantidade} onChange={(event) => updateItem('quantidade', event.target.value)} required />
        </FormField>
        <FormField label="Valor unitario">
          <input className={inputClassName} value={form.itens[0].valor_unitario} onChange={(event) => updateItem('valor_unitario', event.target.value)} required />
        </FormField>
        <FormField label="Desconto item">
          <input className={inputClassName} value={form.itens[0].desconto} onChange={(event) => updateItem('desconto', event.target.value)} />
        </FormField>
      </section>
      <button disabled={saving} className="inline-flex items-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white disabled:opacity-60">
        <Save className="h-4 w-4" />
        {saving ? 'Salvando...' : 'Salvar NF-e'}
      </button>
    </form>
  )
}
